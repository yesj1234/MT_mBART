# Parameter used for this model.

### warmup_ratio

Training이 시작될 때, 모든 parameters들은 보통 random values(initialized)이므로,최종 solution에서 멀리 떨어져 있다.이 때, 너무 큰 learning rate를 사용하면 numerical instability가 발생할 수 있기에,초기에 작은 learning rate를 사용하고, training과정이 안정되면 초기 learning rate로 전환하는 방법.

### gradient_accumulation_steps

한정된 GPU 자원을 이용해 보다 큰 batch size를 활용하기 위한 파라미터. 일반적인 학습에선 매 step 마다의 forward , backward pass 가 한번 이뤄지면 (in mini batch) 가중치(gradient)가 업데이트 되지만 gradient_accumulation_steps 값으로 1보다 큰 값을 설정해주면 해당 값 만큼의 mini batch에서 forward, backward pass 가 끝난 후에 한번에 가중치를 업데이트 함. 예를 들면
4GPU, 8 accumulation steps , 2 per device train batch size일 경우
4 (per device train batch size , mini batch) X 8 (accumulation steps) X 4 (GPUs) = 128 (total batch size)
즉 한정된 GPU 자원으로도 큰 배치 사이즈를 사용 하는 효과를 볼 수 있음.

### eval_accumulation_steps

gradient_accumulation_steps 와 마찬가지로 eval 단계에서도 마찬가지로 설정을 해주어야 함. 따로 설정 해주지 않으면 memory out of error가 날 수 있음.

### fp16

이름에서 유추 할 수 있듯이 floating point format에 관한 파라미터.
fp16은 half-precision의 준말로, 16비트 부동 소수점 형식을 나타냄. 이 형식은 메모리를 적게 사용. 그러나 16비트의 정밀도가 낮아서 모델의 정확도가 떨어질 수 있음. 따라서 모델을 훈련할 때는 일반적으로 fp32(32비트 부동 소수점 형식)를 사용하고, 추론(inference) 단계에서는 fp16을 사용하여 연산 속도를 높이는 경우가 많음. 모델의 특성에 따라 사용 여부를 결정해야 함. mbart의 경우 기본 모델 사이즈가 크기 때문에 메모리 활용을 위해 train 과정에도 fp16을 사용.

### references

(warmup_ratio)[https://arxiv.org/abs/1812.01187]
