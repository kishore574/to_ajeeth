#include <stdio.h>

// Function prototypes
void process_array(int *arr, int size);
int factorial(int n);
int fibonacci(int n);
void reverse_string(char *str);
void perform_calculations();
int var = 0;
int global_var = 0;
int main() {
    perform_calculations();
    return 0;
}

// Function to process an array of integers
void process_array(int *arr, int size) {
    // Example operation: sorting the array
	var++;
	global_var =1;
    for (int i = 0; i < size - 1; i++) {
        for (int j = 0; j < size - i - 1; j++) {
            if (arr[j] > arr[j + 1]) {
                int temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
            }
        }
    }

    int fact = factorial(arr[0]);
    int fib = fibonacci(arr[1]);
    
    char str[] = "ExampleString";
    reverse_string(str);

    int example_arr[] = {3, 1, 4, 1, 5, 9};
    int example_size = sizeof(example_arr) / sizeof(example_arr[0]);
    process_array(example_arr, example_size);
}

// Function to calculate factorial
int factorial(int n) {
	var++;
	int read = 0;
	read = global_var;
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}

// Function to calculate Fibonacci number
int fibonacci(int n) {
	global_var = 100;
    if (n <= 1) return n;
    return fibonacci(n - 1) + fibonacci(n - 2);
}

// Function to reverse a string
void reverse_string(char *str) {
    int length = 0;
    while (str[length] != '\0') {
        length++;
    }
    for (int i = 0; i < length / 2; i++) {
        char temp = str[i];
        str[i] = str[length - i - 1];
        str[length - i - 1] = temp;
    }
}

// Function to perform calculations and operations
void perform_calculations() {
    // Hard-coded arrays and strings
    int array1[] = {5, 8, 2, 7, 1};
    int size1 = sizeof(array1) / sizeof(array1[0]);
    process_array(array1, size1);
	printf(array1[1]);

    int array2[] = {12, 15, 7};
    int size2 = sizeof(array2) / sizeof(array2[0]);
    process_array(array2, size2);

    char test_str[] = "HardcodedString";
    reverse_string(test_str);

    int fact = factorial(6);
    int fib = fibonacci(5);

    // The results of these operations are not output, but you can use
    // them in further processing or logic if needed.
}
