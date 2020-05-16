#!/bin/bash

source /etc/profile

###################################
# Please change these parameters according to your real env.
###################################
# PYTHON_PATH=/usr/local/jdk1.8.0_60
# check PYTHON_PATH
PYTHON_PATH=`whereis python`
if [ x"$PYTHON_PATH" == x ]; then
    echo "==================== Failed! ====================="
    echo "======         Please Install Python       ======"
    echo "=================================================="
    exit 1
fi


# set ulimit
ulimit -s 20480

# application directory
cd `dirname $0`
APP_HOME=`pwd`

APP_NAME="$(cd ${APP_HOME} && find -mindepth 1 -maxdepth 1 -name 'launch_*.py' |awk -F'/' '{print $NF}')"



# path of log file, because logback can't create missing directory, we need to help it by shell script
LOGS_DIR="$APP_HOME/logs"
if [ ! -d $LOGS_DIR ]; then
    mkdir $LOGS_DIR
    #echo "created logs directory: path=$LOGS_DIR"
fi
STDOUT_FILE=$LOGS_DIR/out.log


# waiting timeout for starting, in seconds
START_WAIT_TIMEOUT=30

psid=0

checkpid() {
    psid=$(/bin/ps aux | grep "/$APP_NAME" |grep -v grep |awk '{print $2}')
    echo "psid check: $psid"
    if [[ -z "$psid" ]]; then
       psid=0
    fi
    echo "psid check: $psid"
}


###################################
#(函数)启动程序
 #
 #说明：
 #1. checkpid，刷新$psid全局变量
 #2. 如果程序已经启动（$psid不等于0），则提示程序已启动
 #3. 如果程序没有被启动，则执行启动命令行
 #4. 启动命令执行后，再次调用checkpid函数
 #5. 如果步骤4的结果能够确认程序的pid,则打印[OK]，否则打印[Failed]
 #注意：echo -n 表示打印字符后，不换行
 #注意: "nohup 某命令 >/dev/null 2>&1 &" 的用法
###################################
start() {
   checkpid

   if [ ! -n "$psid" ]; then
      echo "================================"
      echo "warn: $APP_NAME already started! (pid=$psid)"
      echo "================================"
   else
      echo -n "Starting $APP_NAME ..."
      nohup python ${APP_HOME}/${APP_NAME} >>$STDOUT_FILE 2>&1 &
      sleep 1
      checkpid
      echo "psid:".$psid
      if [ ! -n "$psid" ]; then
         echo "(pid=$psid) [OK]"
      else
         echo "[Failed]"
      fi
   fi
}

###################################
#(函数)调试程序
 #
 #说明：
 #1. checkpid，刷新$psid全局变量
 #2. 如果程序已经启动（$psid不等于0），则提示程序已启动
 #3. 如果程序没有被启动，则执行启动命令行
 #4. 启动命令执行后，再次调用checkpid函数
 #5. 如果步骤4的结果能够确认程序的pid,则打印[OK]，否则打印[Failed]
 #注意：echo -n 表示打印字符后，不换行
 #注意: "nohup 某命令 >/dev/null 2>&1 &" 的用法
###################################
debug() {
   checkpid

   if [ ! -n "$psid" ]; then
      echo "================================"
      echo "warn: $APP_NAME already started! (pid=$psid)"
      echo "================================"
   else
      echo -n "Starting $APP_NAME ..."
      nohup python ${APP_HOME}/${APP_NAME} >>$STDOUT_FILE 2>&1 &
      checkpid
      if [ ! -n "$psid" ]; then
         echo "(pid=$psid) [OK]"
      else
         echo "[Failed]"
      fi
   fi
}



###################################
#(函数)停止程序
#
#说明：
#1. 首先调用checkpid函数，刷新$psid全局变量
#2. 如果程序已经启动（$psid不等于0），则开始执行停止，否则，提示程序未运行
#3. 使用kill -9 pid命令进行强制杀死进程
#4. 执行kill命令行紧接其后，马上查看上一句命令的返回值: $?
#5. 如果步骤4的结果$?等于0,则打印[OK]，否则打印[Failed]
#6. 为了防止python程序被启动多次，这里增加反复检查进程，反复杀死的处理（递归调用stop）。
#注意：echo -n 表示打印字符后，不换行
#注意: 在shell编程中，"$?" 表示上一句命令或者一个函数的返回值
###################################
stop() {
   STOP_WAIT_TIME="90"
   checkpid
   if [ ! -z "$psid" ]; then
      echo -n "Stopping $APP_NAME ...(pid=$psid) "
      sudo sh -c "kill $psid"

      let kwait=${STOP_WAIT_TIME}
      count=0;
      until [ ! -z "$psid" ] || [ $count -gt $kwait ]  
      do
          echo -n -e ".";
          sleep 1
          checkpid
          let count=$count+1;
      done
      if [ $count -gt $kwait ];then
          echo -n -e "\nkilling processes which didn't stop after ${STOP_WAIT_TIME} seconds\n"
          sudo sh -c "kill -9 $psid"
      fi
      echo "[OK]"
   else
      echo "================================"
      echo "warn: $APP_NAME is not running"
      echo "================================"
   fi
}


###################################
#(函数)检查程序运行状态
#
#说明：
#1. 首先调用checkpid函数，刷新$psid全局变量
#2. 如果程序已经启动（$psid不等于0），则提示正在运行并表示出pid
#3. 否则，提示程序未运行
###################################
status() {
   checkpid

   if [ ! -n "$psid" ];  then
      echo "$APP_NAME is running! (pid=$psid)"
   else
      echo "$APP_NAME is not running"
   fi
}



###################################
#(函数)打印系统环境参数
###################################
info() {
   checkpid

   echo "System Information:"
   echo "****************************"
   echo `head -n 1 /etc/issue`
   echo `uname -a`
   echo
   echo `python --version`
   echo
   echo "APP_HOME=$APP_HOME"
   echo "APP_NAME=$APP_NAME"
   echo
   if [ ! -n "$psid" ];  then
      echo "Application is running! (pid=$psid)"
   else
      echo "Application is not running"
   fi
   echo "****************************"
}

###################################
#读取脚本的第一个参数($1)，进行判断
#参数取值范围：{start|stop|restart|status|info}
#如参数不在指定范围之内，则打印帮助信息
###################################
case "$1" in
   'debug')
     stop
     debug
     ;;
   'start')
     start
     ;;
   'stop')
     stop
     ;;
   'restart')
     stop
     start
     ;;
   'status')
     status
     ;;
   'info')
     info
     ;;
  *)
     echo "Usage: $0 {debug|start|stop|restart|status|info}"
     exit 1
esac
