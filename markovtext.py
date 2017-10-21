import markovify

with open("markov.txt") as f:
    text = f.read()

text_model = markovify.NewlineText(text, state_size=2)

# Print three randomly-generated sentences of no more than 140 characters
for j in range(3):
    for i in range(5):
        print(text_model.make_short_sentence(60, tries=1000))
    print("\n")
