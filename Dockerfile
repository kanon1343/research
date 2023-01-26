FROM sonoisa/deep-learning-coding:pytorch1.12.0_tensorflow2.9.1

RUN pip install matplotlib \
                scikit-learn \
                pydot \
                graphviz \
                pydotplus \
    && mkdir /home/ubuntu/harada 

COPY ./harada /home/ubuntu/harada
