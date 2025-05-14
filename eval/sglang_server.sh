model=$MODEL_PATH
python -m sglang_router.launch_server \
    --model-path $model \
    --dp-size 8 \
    --mem-fraction-static 0.90 \
    --context-length 32768 \
    --host 127.0.0.1 \
    --port 8001 \
    --show-time-cost \
    --enable-metrics
