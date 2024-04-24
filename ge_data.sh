#!/bin/bash

# 初始化 start 和 end 变量
start=0
end=100

# 循环，直到 start 小于 2000
while [ $start -lt 2000 ]
do
  # 调用 Python 脚本并传递参数
  python ge_data/ge_data_all_vicuna.py --start $start --end $end --outdir /root/Hawk/data/ShareGPT_Vicuna_unfiltered/ || {
    echo "Error occurred - SKIPPING to next batch"
    # 更新 start 和 end 变量
    start=$((start + 100))
    end=$((end + 100))
    
    # 如果 end 大于 2000，我们将其设为 2000
    if [ $end -gt 2000 ]; then
      end=2000
    fi
    
    continue
  }
  
  # 更新 start 和 end 变量
  start=$((start + 100))
  end=$((end + 100))

  # 如果 end 大于 2000，我们将其设为 2000
  if [ $end -gt 2000 ]; then
    end=2000
  fi
done

