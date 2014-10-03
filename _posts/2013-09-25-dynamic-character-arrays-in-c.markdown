---
layout: post
title: Dynamic Character Arrays in C
date: '2013-09-25 16:00:00'
category: programming
tags: [c]
comments: true
---

In my first Data Structures class I was assigned a project where I was required to gather input from a user and then operate on that input to evaluate a mathematical expression. While I was writing the program I discovered how to dynamically allocate memory for an array of characters input from stdin. While I ended up abandoning the technique becuase it wasn’t going to work in that specific project, I wanted to document it here so I wouldn’t forget about it and so that others could benefit from my small insight.

One of my favorite aspects of writing C code has always been the challenge of crafting my code to be as small and efficient as possible. A large part of efficiency in a C program comes from intelligently managing how that program creates and handles its memory during execution. Gathering input from a user at the console presents a few challenges when it comes to memory management. How many characters will the user be allowed to enter? How do you warn your users about the limitations to their input? It can be wasteful to allocate memory for 255 characters if your users will only enter 10 or 50 or even 100.

We can mitigate these challenges by declaring a pointer to a character array and then initializing it with enough space to hold only a single character. By doing this we minimize the amount of memory needed when first compiling and running our program, and then simply resize it dynamically while the user is giving us their input.

The code is rather simple. I've created a single file program that I named `main.c`. It would probably make more sense in a larger program as a function that takes a character pointer as an argument and returns that pointer once it’s complete. Something like:

{% highlight c %}
char *get_user_input(char *input)
{% endhighlight %}

Here's the entire program:

{% highlight c %}
#include <stdio.h>
#include <stdlib.h>
int main(void) {
  int i = 0;
  char c, *input;
  input = (char *) malloc(sizeof(char));

  if(input == NULL) {
    printf("Could not allocate memory!");
    exit(1);
  }
  
  printf("Input a string, press enter when done: ");
  
  while((c = getchar()) != '\n') {
    realloc(input, (sizeof(char)));
    input[i++] = c;
  }

  input[i] = '\0';
  printf("\nYou entered the string: %s\n", input);
}
{% endhighlight %}

If you’d like to run this program for yourself, copy it into a file called `main.c` and run this command in your terminal:

{% highlight c %}
gcc main.c -o main
{% endhighlight %}

We start by declaring an int named `i`. It’s declared and initialized to 0 because its only function will be to serve as an index into our character array. Because we want to start inserting characters at the beginning, `i` needs to be 0. We also need two char variables, `c` will server as the temporary storage location where we can check its value to see if it should be inserted into the array or if the user is done entering their input. The `input` pointer will be the location where we dynamically allocate memory for the user’s input. Some programs might call this a "buffer" instead of input.

The `input` pointer is first initialized with just enough memory to store a single character. The reason for this is two-fold. First, we don’t want to allocate more memory than we need to. A single character is one of the smallest memory types we get from C. Secondly, all "strings" in C should be terminated by a [null character](http://en.wikipedia.org/wiki/Null_character). A string in C is nothing more than a contiguous group of individual characters terminated by the null character. Also, by creating our initial character array with enough space for one character we are ensuring that after we’ve dynamically allocated enough space for the string entered by our user we have one spot left at the end for the NULL.

The call to [`malloc()`](http://www.acm.uiuc.edu/webmonkeys/book/c_guide/2.13.html#malloc), which is how we dynamically initialize memory for a data type at runtime in C, is not guaranteed to return a valid pointer to a properly created memory location. So we next check to see if the input variable is pointing to NULL and if it is we bail out with an error. Once we know we have a pointer to a valid memory location we can ask our user for their input.

After printing the request for input with [`printf()`](http://www.acm.uiuc.edu/webmonkeys/book/c_guide/2.12.html#printf) we enter a [`while()`](http://www.acm.uiuc.edu/webmonkeys/book/c_guide/1.6.html#while) loop which uses [`getchar()`](http://www.acm.uiuc.edu/webmonkeys/book/c_guide/2.12.html#getchar) to grab each character entered by the user one by one. We check to see if it's equal to the newline character ('\n') which indicates the user hit the enter or return key. This tells us that the user is done typing and we can move on past our while loop. If the character is anything besides a newline we want to store it in our array.

This is where the real magic of the C standard library comes into play. Using the [`realloc()`](http://www.acm.uiuc.edu/webmonkeys/book/c_guide/2.13.html#realloc) function we can dynamically resize the memory space used by a data type at runtime. In our case we want to increase the size of the input array by enough to hold the character just entered by the user. This function accepts a pointer to the data type that needs to be resized and the size of the needed reallocation. In our case we pass in the `input` array and the return value of calling [`sizeof(char)`](http://www.acm.uiuc.edu/webmonkeys/book/c_guide/1.2.html#sizeof). This creates a new spot in the array where we can insert the latest character. This is where we use the 'i' variable that we defined at the top of the program. Each time through the loop we make the array larger by one character and insert the character at the index 'i'. Each time we insert a new character 'i' will be incremented by 1 (i++). Once the user presses enter we break out of the loop and use 'i' one more time to insert the null character at the end. We now have an array containing the exact number of characters entered by the user, but we only had to allocated enough space for one character to begin with. Our users can now enter any amount of characters they’d like. We don’t have to warn them about any limitations or initially over allocate space to handle exceptionally large strings. We’ve dynamically allocated the memory as the user typed and can now do whatever we’d like with the string; in our example program we just print the string back out to show that it works they way we expect it to.

I hope you’ve gained a small amount of knowledge from the tip in this short tutorial. When we’re able to properly and efficiently handle the allocation of memory in our programs, everyone benefits. If you’d like to download the code, it’s available on [Github](https://github.com/humanshell/c/tree/master/dynamic_char).