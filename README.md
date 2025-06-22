# Kinkcompare
A tool to compare kink preferences while not revealing that you like something to someone who doesn't.

## Features
Allows comparing kinks between any number of people without revealing any preferences that would be a hard limit for someone else to that person. 

Outputs personalized lists of the other participants' preferences. Options which the user marked as a hard limit are censored. Additionally outputs a common list where only items which are not a hard limit for any participant. 

Supports simple kinks (singles) for which all participants give a preference rating, as well as opposite pairings (doubles) where a user's preference is compared to that of the other participants in the corresponding opposite. (e.g. sub/dom, top/bottom pairings)

## Usage
Run `python kinkcompare.py [options] [names ...]` with the names of the participents as arguments. If no arguments are given, a help text will be printed detailing the options. The following are recognized:

- `-h`, `--help` A help message will be printed.
- `-l`, `--list FILENAME` Specify filename of the kink list to be used. (Default: kinklist.txt)
- `-g`, `--gen-input` Generate the input file the users need to fill out and exit.
- `-u`, `--uncensored` Never censor partner's responses.

First, the users should use `-g` to generate their input files `inputs/input_NAME.txt` and fill them out. Here, they can indicate a preference by rating the given kinks from `0` to `10`, or by indicating a hard limit using `n`. `c` can be used to indicate curiousity and `i` to denote indifference. 

The format of the input file should not be altered and each line should end with the user's rating. Example:
```
Example Kink A - 4
Example Kink B - 2
Example Kink C - n
```

When all participants have filled out their input files, the script can be used to generate comparisons between them. This again requires the user to specify the same kinklist file using `-l FILENAME` as was used to generate the inputs. In general, there will be personalized outputs for each participent, `outputs/output_NAME.txt`, as well as a common output file, `outputs/output_common.txt`.

## Output files
### Personalized output
The basic structure is described in the header. `Kink (your answer) - NAME1's answer - NAME2's answer ...`

For "singles", each line will start with its respective kink, followed by the list's owner's response, followed by the other participants' responses seperated by dashes. For "doubles", each line will start by the two opposite items seperated by `|`, followed by the participants' answers seperated by `|` in the same pattern as for singles.

Unless the `-u` option is specified, if the file owner's response was `n`, the partners' answers for that kink will be censored using `###` in the case of singles. In case of doubles, the partners' answers in the respective opposite category is censored. 

### Common output
The basic structure is described in the header. `Kink - NAME1's answer - NAME2's answer ...`

They are analogously structured to the personalized output files. The difference being in how the censoring is applied. Unless `-u` is specified, if one or more of the users responds to a kink with `n`, that kink is removed from the output file. An exception to this happens when the number of participants is 2. In that case, for doubles, only the partner's answer to the opposite kink is censored. 

## Kinklist formatting
Custom kinklists have to be formatted in the following way: 

The list starts with singles, each in their own line. Then follows a line containing `#####`, after which the doubles are listed, where the opposites are seperated by `;`. Each double line has to contain a `;`. Example:
```
Example Single A
Example Single B
#####
Example Double A Top;Example Double A Bottom
Example Double B Top;Example Double B Bottom
```
