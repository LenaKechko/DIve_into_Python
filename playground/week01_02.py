import sys

count = int(sys.argv[1])

for x in range(1, count + 1):
    print(" " * (count - x) + "#" * x)

# num_steps = int(sys.argv[1])
#
# for i in range(num_steps):
#     print(" " * (num_steps - i - 1), "#" * (i + 1), sep="")