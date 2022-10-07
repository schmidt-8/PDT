import gzip
import shutil
import sys

print(str(sys.argv[1]))
print(str(sys.argv[2]))

with gzip.open(str(sys.argv[1]), 'rb') as f_in:
    with open(str(sys.argv[2]), 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)