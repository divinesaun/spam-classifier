# import spacy
# import pandas as pd
# import random
# import pickle
# from spacy.training import Example

# # Load blank English model
# nlp = spacy.blank("en")

# # Load dataset
# df = pd.read_csv("ecommerce_intent_dataset.csv")

# # Add text categorizer if not exists
# if "textcat" not in nlp.pipe_names:
#     textcat = nlp.add_pipe("textcat")
# else:
#     textcat = nlp.get_pipe("textcat")

# # Get unique labels
# labels = df['intent'].unique()

# # Add labels
# for label in labels:
#     textcat.add_label(label)

# # Prepare training data
# train_data = []
# for index, row in df.iterrows():
#     text = row['text']
#     intent = row['intent']
#     # Create the dictionary of cats where the correct label is 1 and others are 0
#     cats = {label: 1.0 if label == intent else 0.0 for label in labels}
#     train_data.append((text, {"cats": cats}))

# # Begin training
# optimizer = nlp.begin_training()

# print("Beginning training...")
# for epoch in range(15):
#     random.shuffle(train_data)
#     losses = {}
#     for text, annotations in train_data:
#         doc = nlp.make_doc(text)
#         example = Example.from_dict(doc, annotations)
#         nlp.update([example], sgd=optimizer, losses=losses)
#     print(f"Epoch {epoch+1} - Losses: {losses}")

# # Export the model as pkl
# with open("intent_classifier_model.pkl", "wb") as f:
#     pickle.dump(nlp, f)

# print("Model trained and exported as intent_classifier_model.pkl")

