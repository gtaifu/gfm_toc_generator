   - 1.1.1 [h3 level](#h3-level)
 - 2 [h1 header](#h1-header)
  - 2.1 [Good h2 Header](#good-h2-header)
  - 2.2 [The Second h2 Header 中文](#the-second-h2-header-中文)
 - 3 [h1 Header](#h1-header-1)
   - 3.1.1 [Direct h3 Header###](#direct-h3-header)
    - 3.1.1.1 [H4 header](#h4-header)
  - 3.2 [Third h2 header](#third-h2-header)
  - 3.3 [Third h2 header](#third-h2-header-1)

This page links to the inventories of all kinds of generators.

### h3 level
See TomOnTime's comment at https://gist.github.com/asabaylus/3071099

The code that creates the anchors is here:
https://github.com/jch/html-pipeline/blob/master/lib/html/pipeline/toc_filter.rb

1. It downcases the string
2. remove anything that is not a letter, number, space or hyphen (see the source for how Unicode is handled)
3. changes any space to a hyphen.
4. If that is not unique, add "-1", "-2", "-3",... to make it unique


# h1 header
This is good here.
## Good h2 Header
Happy new Year.

## The Second h2 Header
Hello world.

# h1 Header
### Direct h3 Header###

#### H4 header

## Third h2 header
## Third h2 header


