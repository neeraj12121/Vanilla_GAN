import tensorflow as tf
from tensorflow.contrib.layers import xavier_initializer
import numpy as np

##Placeholders
x_ = tf.placeholder(tf.float32, shape=[None, 784], name='x')
z_ = tf.placeholder(tf.float32, shape=[None, 100], name='z')

##Weights and Bias for Discriminator and Generator
DiscriminatorW1 = tf.get_variable('dw1', [784, 128], tf.float32, initializer=xavier_initializer())
DiscriminatorW2 = tf.get_variable('dw2', [128, 1], tf.float32, initializer=xavier_initializer())
DiscriminatorB1 = tf.get_variable('db1', [128], tf.float32, initializer=tf.constant_initializer(0.))
DiscriminatorB2 = tf.get_variable('db2', [1], tf.float32, initializer=tf.constant_initializer(0.))

GeneratorW1 = tf.get_variable('gw1', [100, 128], tf.float32, initializer=xavier_initializer())
GeneratorW2 = tf.get_variable('gw2', [128, 784], tf.float32, initializer=xavier_initializer())
GeneratorB1 = tf.get_variable('gb1', [128], tf.float32, initializer=tf.constant_initializer(0.))
GeneratorB2 = tf.get_variable('gb2', [784], tf.float32, initializer=tf.constant_initializer(0.))


theta_discriminator = [DiscriminatorW1, DiscriminatorW2, DiscriminatorB1, DiscriminatorB2]
theta_generator = [GeneratorW1, GeneratorW2, GeneratorB1, GeneratorB2]
def Discriminator(x):
    dh1 = tf.nn.relu(tf.matmul(x, dw1) + db1)
    logit = tf.matmul(dh1, dw2) + db2
    prob = tf.nn.sigmoid(logit)

    return prob, logit

def Generator(z):
    gh1 = tf.nn.relu(tf.matmul(z, gw1) + gb1)
    log_prob = tf.matmul(gh1, gw2) + gb2
    prob = tf.nn.sigmoid(log_prob)

    return prob



generator_sample = Generator(z_)
real_prob, real_logit = Discriminator(x_)
fake_prob, fake_logit = Discriminator(generator_sample)


#loss
discriminator_loss_real = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits=real_logit, labels=tf.ones_like(real_logit)))
discriminator_loss_fake = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits=fake_logit, labels=tf.zeros_like(fake_logit)))
discriminator_loss = discriminator_loss_real+discriminator_loss_fake
generator_loss = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits=fake_logit, labels=tf.ones_like(fake_logit)))

#training
d_train_op = tf.train.AdamOptimizer().minimize(d_loss, var_list=theta_d)
g_train_op = tf.train.AdamOptimizer().minimize(g_loss, var_list=theta_g)
