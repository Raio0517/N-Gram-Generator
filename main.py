import random, pickle, os.path

ngrams = {}
max_gram_length = 5
build_mode = False

files = ["TYW.txt"]

def create_ngram(line, n):
  line = line.strip().split(' ')
  line.append("EOL")
  for i in range(len(line)-(n-1)):
    key = line[i]
    for j in range(1, n-1):
      key += " " + line[i+j]
    if key in ngrams:
      if line[i+(n-1)] in ngrams[key]:
        ngrams[key][line[i+(n-1)]] += 1
    else:
      ngrams[key] = {line[i+(n-1)]: 1}

def read_file(file_name):
  in_file = open(file_name, "r")
  for line in in_file:
    for i in range(2, max_gram_length):
      create_ngram(line, i)

def generate_sentence(words, key):
  sentence = key
  count = 0
  while True:
    key_list = list(ngrams[key].keys())
    next_word = random.choice(key_list)
    if next_word == "EOL":
      sentence += "."
      break
    sentence += ' ' + next_word
    words.append(next_word)

    if len(words) == max_gram_length or build_mode:
      words.pop(0)
    key = words[0] + "".join(" "+words[i] for i in range(1, len(words)))
    count += 1
    if count % 20 == 0:
      sentence += "\n"
  print(sentence+"\n")

def save_ngrams():
  f = open("ngrams.pkl", "wb")
  pickle.dump(ngrams, f)
  f.close()

def load_ngrams():
  global ngrams
  f = open("ngrams.pkl", "rb")

def main():
  if os.path.isfile("ngram.pkl"):
    load_ngrams()
  else:
    for file in files:
      read_file(file)
    save_ngrams()

print("Welcome to sentence generator.\n")
key_list = list(ngrams.keys())

while True:
  ui = input("Enter the first 1 to {} words of a sentence: ".format(max_gram_length - 1)).split(" ")
  key = ui[0]+"".join(" " + ui[i] for i in range(1, len(ui)))
  print("")
  if key == "quit":
    break
  if key == "random":
    key = random.choice(key_list)
    print("Key: " + key + "\n")
    generate_sentence(key.split(" "), key)
  elif key in ngrams:
    generate_sentence(ui, key)
  else:
    print("not found\n")

if __name__ == "__main__":
  main()
