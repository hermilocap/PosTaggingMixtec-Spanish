# Automatic Grammatical Tagger for a Spanish-Mixtec Parallel Corpus
It is an intelligent tagger of Spanish-Mixtec parallel corpora using CRF, LSTM and Transformers. It allows you to train new neural network and CRF models and then incorporate these new models into the application to generate labeled texts. This functionality allows you to have an intelligent labeler since the new data is added to the training data and allows you to improve precision.

The application is capable of generating synthetic text labels in the Mixtec language using GPT-4 and GPT-4O.
The tagged text generated is a useful resource for the development of technologies for other languages ​​with low digital resources, development of automatic translation systems, voice recognition, among other tools.
## Installation
1. Clone the repository
```bash
git clone https://github.com/hermilocap/PosTaggingMixtec-Spanish.git
```
2. Navigate to the project directory
```bash
cd PosTaggingMixtec-Spanish
```  
2. Generate the environment using <br />
```bash
python -m venv env
```
Activate env. If you work on Windows
```bash
env\Scripts\activate.ps1
```
or
```bash
env\Scripts\activate
```
3. Install the libraries from the archive using <br />
```bash
python -m pip install -r requirements.txt
```
## Usage

First, it is necessary to know the subdirectory and files that the project contains.<br />
**Data:** The data directory, where it contains the training file train.txt and the output tags.txt file.

* Train.txt. File must contain one sentence per line. The maximum number of sentences allowed is 25 sentences. As indicated below.
Train file must contain one sentence per line. As indicated below
```bash
Yaa yìì Ñuu Kò’yó.
NàÑuu Kò’yó nàndà’yìyó kuàtyi
nákoo tì’va kàa xí’ín kuáyì
tandà nìkisiin miímà’ñú ñu’ùn
ndànìsìsò nìka’ndi tùxìí.
Katúúnyó xìnì yiváyó yùkù kuíì
ñàkoo viiyó, xí’ín yi’ya kúuñà và’a
tyiñàndiví, nìnì’ìn tá’vikún kandú’ukún
xí’ín nduku nda’à yi’ya kà’yirañà.
Tàa ñinka ñuu kàtyira kani tná’anyó
taxí’ín xà’àrá nìxàñùrà nùù ñú’ùnkún
naki’in xìnìkún, yiváyó tyíndiví
ñii sè’e nàñuu tàxina kundaa yó’ó.
```
* Tags.txt. Contains the output format. An example is shown below:
```bash
Yaa#DA0MS0
yìì#NCMS000
Ñuu#NP00000
Kò’yó#VMSI3S0
.#Fp
NàÑuu#DA0MS0
Kò’yó#VMSI3S0
nàndà’yìyó#NCMS000
kuàtyi#NCFS000
nákoo#RN
tì’va#NCFS000
kàa#CC
xí’ín#DA0FS0
kuáyì#NCFS000
tandà#VMN0000
nìkisiin#NCMS000
miímà’ñú#NCMS000
ñu’ùn#NCMS000
ndànìsìsò#NCMS000
nìka’ndi#VMN0000
tùxìí#NCMS000
.#Fp
```
**ExeFiles.** Contains the application executable. You must access the <code>dist\AITagger</code> directory and run AITagger. <br />
**Notebooks:** Contains 3 Google Colab notebooks for CRF training. LSTM, and Transformers. <br />
1. Add environment variables.
If you have Windows 11 you must access <code>Settings/Advanced system settings/Environment variables</code><br />
Next add 2 new environment variables.<br />
The first is the GPT key and the second is the name of the GPT model to use.<br />
Variable name: KEYGPT, MODELGPT <br />
Variable value: Your GPT key <br />
3. Run the tool as:
```bash
python AITagger.py
```
3. Tagged. The main screen of the project is then displayed.<br />
![window](https://github.com/user-attachments/assets/3238f806-fadb-4823-9157-57bac02e165c)
Each of the steps to follow to label a corpus are detailed below.<br />
   1.-Select path of your input file.<br />
   2.- Select path of you input file.<br />
   3.- Press on AITagger for start.<br />
   4.-App show results and generate output file.<br />
