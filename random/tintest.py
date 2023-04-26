import tensorflow as tf

inputs = tf.random.normal([32, 10, 8])
print("inputs")
print(inputs)
lstm = tf.keras.layers.LSTM(4)
output = lstm(inputs)
print(output.shape)
print(output)

lstm = tf.keras.layers.LSTM(4, return_sequences=True, return_state=True)
whole_seq_output, final_memory_state, final_carry_state = lstm(inputs)
print(whole_seq_output.shape)

print(final_memory_state.shape)

print(final_carry_state.shape)

