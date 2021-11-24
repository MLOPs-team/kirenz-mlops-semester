---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.11.5
kernelspec:
  display_name: Python 3.9.7 64-bit (windows store)
  name: python3
---

# Jupyter-Book good to know

## General Information

All files are in the folder docs.

+++

## Sections in a file

```{code-cell}
# Chapter 1 title

## Chapter 1 second header

### Chapter 1 third header

#### Chapter 1 section title

##### Chapter 1 section second header
```

### Table of Content

The title '# Chapter 1 Title' of the file is listed in the table of contents (see on the left)

The second, third.... header ist listed in the table of comtents on the top right hand corner

If you added a new file in the learning diary or technical documentation, you also need to update the _toc.yml.
You just need to add the added file in the expecting chapter.

+++

#### How to build the Jupyter-Book

```{code-cell}

```

```{code-cell}
jupyter-book build --all jupyter-book/
```
