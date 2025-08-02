# src/model.py
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Embedding, Conv1D, Bidirectional, LSTM, Dense, Dropout

def build_model(vocab_size: int, embedding_dim: int, max_length: int) -> Model:
    """
    Builds and compiles the CNN-BiLSTM model using the Keras Functional API,
    based on the architecture from your notebook.

    Args:
        vocab_size (int): The size of the vocabulary from the tokenizer.
        embedding_dim (int): The dimension of the embedding vectors.
        max_length (int): The maximum length of the input sequences.

    Returns:
        Model: The compiled Keras model.
    """
    # Input layer expects sequences of a fixed length
    input_layer = Input(shape=(max_length,))
    
    # Embedding layer turns word indices into dense vectors of a fixed size.
    # 'trainable=True' allows the model to fine-tune word embeddings during training.
    embedding_layer = Embedding(input_dim=vocab_size,
                              output_dim=embedding_dim,
                              input_length=max_length,
                              trainable=True)(input_layer)

    # 1D Convolutional layer to extract local features (like n-grams) from sequences.
    cnn_layer = Conv1D(filters=64, kernel_size=7, activation='relu')(embedding_layer)
    
    # Bidirectional LSTM layer processes the sequence in both forward and backward
    # directions to capture context from both past and future words.
    lstm_layer = Bidirectional(LSTM(128))(cnn_layer)
    
    # Dropout layer to prevent overfitting by randomly setting a fraction of input units to 0.
    dropout_layer = Dropout(0.2)(lstm_layer)
    
    # A standard fully-connected (Dense) layer for further processing.
    dense_layer = Dense(64, activation='relu')(dropout_layer)
    
    # Output layer with 3 units (for negative, neutral, positive) and softmax activation
    # to output a probability distribution over the classes.
    output_layer = Dense(3, activation='softmax')(dense_layer)
    
    model = Model(inputs=input_layer, outputs=output_layer)

    # Compile the model with loss function suitable for integer labels, the Adam optimizer,
    # and accuracy as the evaluation metric.
    model.compile(loss='sparse_categorical_crossentropy', 
                  optimizer='adam', 
                  metrics=['accuracy'])
    
    # Print a summary of the model architecture to the console during training.
    print("--- Model Architecture ---")
    model.summary()
    print("--------------------------")
    
    return model

