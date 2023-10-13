# text-abbreviate

`text-abbreviate` is a Python package for string processing. It allows you to clean up and transform strings into the desired format.

## Installation

```bash
pip install my_string_processor
```

## Usage

```python
from text_abbtreviate import process_string

# Example of string processing
print(process_string("Hello, World!")) #HlW
print(process_string("Hello, World!", length=5)) #HllWr
print(process_string("Hello, World!", length=5, keep_separators=True)) #Hl, W
print(process_string("Hello, World!", length=9, keep_separators=True, strict=False)) #Hll, Wrld
print(process_string("Hello, World!", length=9, keep_separators=True, strict=False)) #Hll, Wrld
``` 

## Contributing
If you find a bug or want to add new features, contributions are welcome. Please check the contribution guidelines for more details.

## License
This project is licensed under the MIT License.


