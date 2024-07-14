# Import necessary modules
from tkinter.font import Font
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext as st
from tkinter import filedialog as fd
from tkinter import messagebox as mb
import os,re
from openai import OpenAI
from openai import OpenAIError
import json

class TaggingFiles:
    """
    A class to create a graphical user interface (GUI) for an automatic grammatical tagger for a Spanish-Mixtec parallel corpus.

    Attributes:
        window (tk.Tk): The main window of the GUI.
        client (OpenAI): The OpenAI client initialized with the API key.
        filenamePreproces (str): The filename for preprocessed files.
        modelname (str): The model name retrieved from the environment variable.
        selection (dict): A dictionary to hold the selected tag information.
        nameFileOuPut (str): The output file name.
        nameFileInput (str): The input file name.
        filecontent (str): The content of the input file.
        response (any): The response placeholder.
        responseGPT (any): The response from the GPT model.
        strMessage (str): A string message placeholder.
        ai_response_msg_processing_Exception (str): Exception message for AI response processing.
        font1 (Font): The font used in the GUI.
        message (list): A list to hold messages.
        grammatical_category (list): A list of part-of-speech (POS) tags.
        grammatical_category_mapping (dict): A mapping dictionary for POS tags.
        additional_tags_mapping (dict): A mapping dictionary for additional tags.
        additional_tags (list): A list of additional tags.
        genders (list): A list of genders.
        genres_mapping (dict): A mapping dictionary for genders.
        modes (list): A list of modes.
        mapping_modes (dict): A mapping dictionary for modes.
        numbers (list): A list of numbers.
        mapping_numbers (dict): A mapping dictionary for numbers.
        times (list): A list of times.
        mapping_times (dict): A mapping dictionary for times.
        people (list): A list of people.
        people_mapping (dict): A mapping dictionary for people.
        preposition_forms (list): A list of preposition forms.
        forms_preposition_mapping (dict): A mapping dictionary for preposition forms.
        PronounsCase (list): A list of pronoun cases.
        PronounsCase_mapping (dict): A mapping dictionary for pronoun cases.
        labelframefiles (ttk.LabelFrame): The file selection frame.
        labelpathinput (tk.Label): The label for input file path.
        labelpathoutput (tk.Label): The label for output file path.
        labelframecorpus (ttk.LabelFrame): The corpus display frame.
        scrolledtext1 (st.ScrolledText): The scrolled text widget for displaying the corpus.
        labelframetagg (ttk.LabelFrame): The tag modification frame.
        combo_tags (ttk.Combobox): The combo box for POS tags.
        combo_tags_type (ttk.Combobox): The combo box for additional tags.
        combo_grade_tags (ttk.Combobox): The combo box for tag degrees.
        gender_combo (ttk.Combobox): The combo box for gender.
        combo_mode (ttk.Combobox): The combo box for mode.
        combo_number (ttk.Combobox): The combo box for number.
        combo_time (ttk.Combobox): The combo box for time.
        combo_person (ttk.Combobox): The combo box for person.
        combo_form_preposition (ttk.Combobox): The combo box for preposition form.
        combo_pronoun_case (ttk.Combobox): The combo box for pronoun case.
        labelframeSaveTagg (ttk.LabelFrame): The save tags frame.
        selected_text (tk.StringVar): The variable to hold the selected text.
        textbox_selected_text (tk.Entry): The entry widget for displaying selected text.
        button_save_tag (tk.Button): The button to save tags.
        add_dictionary_button (tk.Button): The button to save tags to the dictionary.
        selected_tag (str): The selected tag.
    """

    def __init__(self):
        """
        Initializes the TaggingFiles class by setting up the main window, initializing the attributes, and starting the main loop.
        """
        self.window=tk.Tk()
        #KEYGPT: is the name of the environment variable
        self.client = OpenAI(api_key=os.environ.get("KEYGPT"))
        self.filenamePreproces=""
        #MODELGPT: is the name of the GPT model
        self.modelname=os.environ.get("MODELGPT")
        self.selection={}
        self.nameFileOuPut=''
        self.nameFileInput=''
        self.filecontent=''
        self.response=any
        self.responseGPT=any
        self.strMessage=''
        self.ai_response_msg_processing_Exception=''
        self.window.title("Automatic Grammatical Tagger for a Spanish-Mixtec Parallel Corpus")
        self.window.resizable(0,0)
        self.font1=Font(family="Arial", size=12)
        self.message= []
        

        # List of POS tags
        self.grammatical_category = [
            "ADJETIVOS", "ADVERBIOS", "ARTÍCULOS", "DETERMINANTES", "NOMBRES",
            "VERBOS", "PRONOMBRES", "CONJUNCIONES", "NUMERALES", "INTERJECCIONES",
            "ABREVIATURAS", "PREPOSICIONES", "SIGNOS DE PUNTUACIÓN"
        ]

        # Mapping for POS tags
        self.grammatical_category_mapping = {
            "A": {"Categoria": "ADJETIVO"},
            "R": {"Categoria": "ADVERBIOS"},
            "T": {"Categoria": "ARTÍCULOS"},
            "D": {"Categoria": "DETERMINANTES"},
            "N": {"Categoria": "NOMBRES"},
            "V": {"Categoria": "VERBOS"},
            "P": {"Categoria": "PRONOMBRES"},
            "C": {"Categoria": "CONJUNCIONES"},
            "M": {"Categoria": "NUMERALES"},
            "I": {"Categoria": "INTERJECCIONES"},
            "Y": {"Categoria": "ABREVIATURAS"},
            "S": {"Categoria": "PREPOSICIONES"},
            "F": {"Categoria": "SIGNOS DE PUNTUACIÓN"}
        }

        # # Additional tags mapping
        self.additional_tags_mapping = {
             "Q":{"Tipo":"Calificativo"},
             "G":{"Tipo","General"}, 
             "D":{"Tipo","Definido"}, 
             "D":{"Tipo","Demostrativo D"},
             "P":{"Tipo","Posesivo P"},
             "T":{"Tipo","Interrogativo T"},
             "E":{"Tipo","Exclamativo E"}, 
             "I":{"Tipo","Indefinido I"},
             "C":{"Tipo","Común C"},
             "P":{"Tipo","Propio P"},
             "M":{"Tipo","Principal M"}, 
             "A":{"Tipo","Auxiliar A"}, 
             "P":{"Tipo","Personal P"},
             "X":{"Tipo","Posesivo X"},
             "R":{"Tipo","Relativo R"},
             "C":{"Tipo","Coordinada C"}, 
             "S":{"Tipo","Subordinada S"},
             "C":{"Tipo","Cardinal C"}, 
             "O":{"Tipo","Ordinal O"},
             "P":{"Tipo","Preposición"}
             }
        
        # Additional tags
        self.additional_tags = [
            "Calificativo", 
            "General", 
            "Definido", 
            "Demostrativo D", 
            "Posesivo P",
            "Interrogativo T", 
            "Exclamativo E", 
            "Indefinido Común C", 
            "Propio P",
            "Principal M", 
            "Auxiliar A", 
            "Personal P", 
            "Demostrativo D", 
            "Posesivo X",
            "Indefinido I", 
            "Interrogativo T", 
            "Relativo R", 
            "Coordinada C", 
            "Subordinada S",
            "Cardinal C", 
            "Ordinal O", 
            "Preposición", 
            "Apreciativo"
        ]

         # List of genders
        self.genders = [
            "Masculino M",
            "Femenino F",
            "Común C"
        ]
        
        # Mapping for genders
        self.genres_mapping = {
            "M":{"Generos","Masculino M"},
            "F":{"Generos","Femenino F"},
            "C":{"Generos","Común C"}
            }

        # List of modes
        self.modes = [
            "Indicativo I",
            "Subjuntivo S",
            "Imperativo M",
            "Condicional C",
            "Infinitivo N",
            "Gerundio G",
            "Participio P"
        ]

        # Mapping for modes
        self.mapping_modes = {
           "I":{"Modos","Indicativo I"},
           "S":{"Modos","Subjuntivo S"},
           "M":{"Modos","Imperativo M"},
           "C":{"Modos","Condicional C"},
           "N":{"Modos","Infinitivo N"},
           "G":{"Modos","Gerundio G"},
           "P":{"Modos","Participio P"}
        }
        
        # List of numbers
        self.numbers = [
            "Singular S",
            "Plural P"
        ]

        # Mapping for modes
        self.mapping_numbers = {
            "S":{"Numeros","Singular S"},
            "P":{"Numeros","Plural P"}
            }
        
        # List of times
        self.times = [
            "Presente P",
            "Imperfecto I",
            "Futuro F",
            "Pasado S"
        ]

        # Mapping for times
        self.mapping_times = {
            "P":{"Tiempos","Presente P"  },  
            "I":{"Tiempos","Imperfecto I"},
            "F":{"Tiempos","Futuro F"    },
            "S":{"Tiempos","Pasado S"    }
            }
        
         # List of people
        self.people = [
            "Primera 1",
            "Segunda 2",
            "Tercera 3"
        ]

        # Mapping for people
        self.people_mapping = {
            "1":{"Personas","Primera 1"},
            "2":{"Personas","Segunda 2"},
            "3":{"Personas","Tercera 3"}
            }
        
        # List of preposition forms
        self.preposition_forms = [
            "Simple S",
            "Contraída C"
        ]

        # Mapping for preposition forms
        self.forms_preposition_mapping = {
           "S":{"Formas","Simple S"},
           "C":{"Formas","Contraída C"}
        }

        # List of pronoun cases
        self.PronounsCase=["Nominativo N", 
                             "Acusativo A", 
                             "Dativo D", 
                             "Oblicuo O"
        ]

        # Mapping for pronoun cases
        self.PronounsCase_mapping={
            "N":{"PronombreCaso","Nominativo N"},
            "A":{"PronombreCaso","Acusativo A"},
            "D":{"PronombreCaso","Dativo D"},
            "O":{"PronombreCaso","Oblicuo O"}
        }

        # Initialize the GUI frames and start the main loop                  
        self.GetFiles()     
        self.GetFrameCorpus()
        self.GetFrameTagg()    
        self.window.mainloop()
    
    def set_selection(self,mapping,tag):
        """
        Sets the selection based on the provided mapping and tag.

        Args:
            mapping (dict): The dictionary containing the mapping information.
            tag (str): The tag to be matched with the mapping.

        Returns:
            dict: The updated selection dictionary.
        """
        selection = {}
        for caracter, opciones in mapping.items():
            if caracter in tag:
                selection.update(opciones)
        return selection
        
    def set_comboboxes(self,tag):
        """
        Sets the combo box values based on the selected tag.

        Args:
            tag (str): The selected tag.
        """
        if tag[0] =="N":
            self.selection= self.set_selection(self.grammatical_category_mapping,tag)

        self.combo_tags.set(self.selection.get("Categoria", ""))
        self.combo_tags.set(self.selection.get("Generos", ""))
        self.combo_tags.set(self.selection.get("Modos", ""))
        self.combo_tags.set(self.selection.get("Numero", ""))
        self.combo_tags.set(self.selection.get("Tiempos", ""))
        self.combo_tags.set(self.selection.get("Personas", ""))
        self.combo_tags.set(self.selection.get("Formas", ""))
        self.combo_tags.set(self.selection.get("PronombreCaso", ""))
    
    def GetFiles(self):
        """
        Creates the file selection frame and its widgets.
        """
        self.labelframefiles=ttk.LabelFrame(self.window, text="Corpus Selection")        
        self.labelframefiles.grid(row=0, column=0, padx=2, pady=2)
        
        self.label1=tk.Label(self.labelframefiles,text="Choose your input file",font=self.font1)
        self.label1.grid(column=0,row=0,padx=2, pady=2)
        
        self.button1=tk.Button(self.labelframefiles, font=self.font1, bg="blue", fg="white",  text="Browse File", command=self.openFile)
        self.button1.grid(column=1, row=0,padx=2, pady=2)
        
        self.buttonborrarpathinput=tk.Button(self.labelframefiles, font=self.font1, bg="blue", fg="white",  text="Delete", command=self.DeleteFileInput)
        self.buttonborrarpathinput.grid(column=2, row=0,padx=2, pady=2)

        self.labelpathinput=tk.Label(self.labelframefiles,font=self.font1)
        self.labelpathinput.grid(row=1, column=0, columnspan=3, padx=2, pady=2)
        
        self.label2=tk.Label(self.labelframefiles,text="Choose output file",font=self.font1)
        self.label2.grid(row=2, column=0, padx=2, pady=2)
        
        self.button1=tk.Button(self.labelframefiles,font=self.font1, bg="blue", fg="white", text="Browse File", command=self.saveFile)
        self.button1.grid(row=2, column=1, padx=2, pady=2)

        self.buttonborrarpathout=tk.Button(self.labelframefiles, font=self.font1, bg="blue", fg="white",  text="Delete", command=self.DeleteFileOut)
        self.buttonborrarpathout.grid(row=2, column=2, padx=2, pady=2)

        self.labelpathoutput=tk.Label(self.labelframefiles,font=self.font1)
        self.labelpathoutput.grid(row=3, column=0, columnspan=3, padx=2, pady=2)

        self.label3=self.label2=tk.Label(self.labelframefiles,text="Press on button AI Tagger to start",font=self.font1)
        self.label3.grid(row=4, column=0, columnspan=3, pady=2)

        self.button1=tk.Button(self.labelframefiles, font=self.font1, bg="green", fg="white", text=" AI Tagger", command=self.taggerFile)
        self.button1.grid(row=5, column=0, columnspan=3, pady=20)

    def GetFrameCorpus(self):
        """
        Creates the frame for displaying the corpus and its widgets.
        """
        self.labelframecorpus=ttk.LabelFrame(self.window, text="Pos Tagging")        
        self.labelframecorpus.grid(row=0, column=1, padx=2, pady=2)

        self.labeltitle=tk.Label(self.labelframecorpus,text="Pos tagging results",font=self.font1)
        self.labeltitle.grid(row=0, column=1, columnspan=3, pady=2)
        
        self.scrolledtext1=st.ScrolledText(self.labelframecorpus,font=self.font1)
        # Bind the click event to the function to capture the selection
        self.scrolledtext1.bind("<ButtonRelease-1>", self.select_tagg)
        self.scrolledtext1.grid(row=1, column=1, columnspan=3, padx=2, pady=2)
        
    def GetFrameTagg(self):
        """
        Creates the frame for displaying the tags and its widgets.
        """
        self.labelframetagg=ttk.LabelFrame(self.window, text="Tag Modification")        
        self.labelframetagg.grid(row=2, column=0, padx=2, pady=2)

        # Add a ComboBox and fill it with POS tags
        self.labeltitle=tk.Label(self.labelframetagg,text="Choose Category",font=self.font1)
        self.labeltitle.grid(row=3, column=0, padx=2, pady=2)
        self.combo_tags = ttk.Combobox( self.labelframetagg, values=self.grammatical_category)
        self.combo_tags.grid(row=3, column=1, padx=2, pady=2)

        # Add an additional ComboBox with specific tags
        self.labeltitle=tk.Label(self.labelframetagg,text="Choose a Type",font=self.font1)
        self.labeltitle.grid(row=4, column=0, padx=2, pady=2)
        self.combo_tags_type = ttk.Combobox(self.labelframetagg, values=self.additional_tags)
        self.combo_tags_type.grid(row=4, column=1, padx=2, pady=2)

        # Add another ComboBox with additional tags
        self.labeltitle=tk.Label(self.labelframetagg,text="Choose a Degree",font=self.font1)
        self.labeltitle.grid(row=5, column=0, padx=2, pady=2)
        self.combo_grade_tags = ttk.Combobox(self.labelframetagg, values=["Apreciativo"])
        self.combo_grade_tags.grid(row=5, column=1, padx=2, pady=2)

        # Add a ComboBox for gender
        self.labeltitle=tk.Label(self.labelframetagg,text="Choose a Gender",font=self.font1)
        self.labeltitle.grid(row=6, column=0, padx=2, pady=2)
        self.gender_combo = ttk.Combobox(self.labelframetagg, values=self.genders)
        self.gender_combo.grid(row=6, column=1, padx=2, pady=2)

        # Add a ComboBox for mode
        self.labeltitle=tk.Label(self.labelframetagg,text="Choose a Mode",font=self.font1)
        self.labeltitle.grid(row=7, column=0, padx=2, pady=2)
        self.combo_mode = ttk.Combobox(self.labelframetagg, values=self.modes)
        self.combo_mode.grid(row=7, column=1, padx=2, pady=2)
        
        # Add a ComboBox for number
        self.labeltitle=tk.Label(self.labelframetagg,text="Choose a Number",font=self.font1)
        self.labeltitle.grid(row=3, column=2, padx=2, pady=2)
        self.combo_number = ttk.Combobox(self.labelframetagg, values=self.numbers)
        self.combo_number.grid(row=3, column=3, padx=2, pady=2)

        # Add a ComboBox for times
        self.labeltitle=tk.Label(self.labelframetagg,text="Choose Verbal Tense",font=self.font1)
        self.labeltitle.grid(row=4, column=2, padx=2, pady=2)
        self.combo_time = ttk.Combobox(self.labelframetagg, values=self.times)
        self.combo_time.grid(row=4, column=3, padx=2, pady=2)

        # Add a ComboBox for person
        self.labeltitle=tk.Label(self.labelframetagg,text="Choose a Person",font=self.font1)
        self.labeltitle.grid(row=5, column=2, padx=2, pady=2)
        self.combo_person = ttk.Combobox(self.labelframetagg, values=self.people)
        self.combo_person.grid(row=5, column=3, padx=2, pady=2)

        # Add a ComboBox for the preposition form
        self.labeltitle=tk.Label(self.labelframetagg,text="Choose a Preposition",font=self.font1)
        self.labeltitle.grid(row=6, column=2, padx=2, pady=2)
        self.combo_form_preposition = ttk.Combobox(self.labelframetagg, values=self.preposition_forms)
        self.combo_form_preposition.grid(row=6, column=3, padx=2, pady=2)

        self.labeltitle=tk.Label(self.labelframetagg,text="Choose a Case",font=self.font1)
        self.labeltitle.grid(row=7, column=2, padx=2, pady=2)
        self.combo_pronoun_case = ttk.Combobox(self.labelframetagg, values=self.PronounsCase)
        self.combo_pronoun_case.grid(row=7, column=3, padx=2, pady=2)
        
        self.SaveFrame()

        self.combo_time.config(state="disabled")
        self.combo_mode.config(state="disabled")
        self.combo_number.config(state="disabled")
        self.combo_person.config(state="disabled")
        self.combo_tags_type.config(state="disabled")
        self.gender_combo.config(state="disabled")
        self.combo_tags.config(state="disabled")
        self.combo_grade_tags.config(state="disabled")
        self.combo_form_preposition.config(state="disabled")
        self.combo_pronoun_case.config(state="disabled")
        # Bind the ComboBox selection change event combo_tags
        self.combo_tags.bind("<<ComboboxSelected>>", self.enable_comboboxes)

    def SaveFrame(self):
        """
        Creates the frame for saving tags and its widgets.
        """
        self.labelframeSaveTagg=ttk.LabelFrame(self.window, text="Save tags")        
        self.labelframeSaveTagg.grid(row=2, column=1, padx=2, pady=2)
        # Add a TextBox to display the selected text
        self.labeltitle=tk.Label(self.labelframeSaveTagg,text="Modify your tag and save",font=self.font1)
        self.labeltitle.grid(row=3, column=1, padx=2, pady=2,columnspan=3)
       
        self.selected_text = tk.StringVar()
        self.textbox_selected_text = tk.Entry(self.labelframeSaveTagg, textvariable=self.selected_text, state="readonly",font=self.font1)
        self.textbox_selected_text.grid(row=4, column=1, padx=2, pady=2, columnspan=3)

        # Add buttons to save tag and add to dictionary
        self.labeltitle=tk.Label(self.labelframeSaveTagg,text="Press on button for save",font=self.font1)
        self.labeltitle.grid(row=5, column=1, padx=2, pady=2)
       
        self.button_save_tag = tk.Button(self.labelframeSaveTagg, text="Save Tag",bg="blue", fg="white",font=self.font1,  command=self.save_tag)
        self.button_save_tag.grid(row=5, column=2, padx=2, pady=2)
       
        self.add_dictionary_button = tk.Button(self.labelframeSaveTagg, text="Save to dictionary",font=self.font1, bg="blue", fg="white", command=self.add_to_dictionary)
        self.add_dictionary_button.grid(row=5, column=3, padx=2, pady=2)

    def add_to_dictionary():
        """
        Adds the modified tag to the dictionary.
        """
        pass
    
    def save_tag():
        """
        Saves the modified tag.
        """
        pass

    def select_tagg(self,event):
        """
        Retrieves the selected text range in the scrolled text widget and updates the combo boxes.

        Args:
            event (tk.Event): The event object for the selection.
        """
        selection = self.scrolledtext1.tag_ranges(tk.SEL)
        if selection:
            # Enable the selected text textbox
            self.textbox_selected_text.config(state="normal")
            # Get the selected text
            self.selected_tag = self.scrolledtext1.get(*self.scrolledtext1.tag_ranges(tk.SEL))
             # Split the selected text by "#" to extract the tag
            tag=self.selected_tag.split("#")
            # Set the comboboxes according to the extracted tag
            if len(tag)>1:
                self.set_comboboxes(str(tag[1]))
            else:
                mb.showwarning("Information", "Please, Choose any tag")
            # Set the selected text variable
            self.selected_text.set(self.selected_tag)

    def enable_comboboxes_Adjectives(self):
        """
        Enables the combo boxes relevant to adjectives and disables irrelevant combo boxes.
        """
        self.combo_tags_type.config(state="normal")
        self.combo_grade_tags.config(state="normal")
        self.gender_combo.config(state="normal")
        self.combo_number.config(state="normal")

        # Disable irrelevant comboboxes for adjectives
        self.combo_mode.config(state="disabled")
        self.combo_pronoun_case.config(state="disabled")
        self.combo_form_preposition.config(state="disabled")
        self.combo_time.config(state="disabled")
        
    def enable_comboboxes_Adverbs(self):
        """
        Enables the combo boxes relevant to adverbs and disables irrelevant combo boxes.
        """
        self.combo_tags_type.config(state="normal")
        
        # Disable irrelevant comboboxes for adverbs
        self.combo_mode.config(state="disabled")
        self.combo_pronoun_case.config(state="disabled")
        self.combo_form_preposition.config(state="disabled")
        self.combo_grade_tags.config(state="disabled")
        self.gender_combo.config(state="disabled")
        self.combo_number.config(state="disabled")
        self.combo_time.config(state="disabled")

    def enable_comboboxes_Articles(self):
        """
        Enables the combo boxes relevant to articles and disables irrelevant combo boxes.
        """
        self.combo_tags_type.config(state="normal")
        self.gender_combo.config(state="normal")
        self.combo_number.config(state="normal")
        
        # Disable irrelevant comboboxes for articles
        self.combo_mode.config(state="disabled")
        self.combo_pronoun_case.config(state="disabled")
        self.combo_form_preposition.config(state="disabled")
        self.combo_grade_tags.config(state="disabled")
        self.combo_person.config(state="disabled")
        self.combo_time.config(state="disabled")

    def enable_comboboxes_Determinants(self):
        """
        Enables the combo boxes relevant to determinants and disables irrelevant combo boxes.
        """
        self.combo_tags_type.config(state="normal")
        self.combo_person.config(state="normal")
        self.gender_combo.config(state="normal")
        self.combo_number.config(state="normal")
        
        # Disable irrelevant comboboxes for determinants
        self.combo_mode.config(state="disabled")
        self.combo_pronoun_case.config(state="disabled")
        self.combo_form_preposition.config(state="disabled")
        self.combo_grade_tags.config(state="disabled")
        self.combo_time.config(state="disabled")

    def enable_comboboxes_Names(self):
        """
        Enables the combo boxes relevant to names and disables irrelevant combo boxes.
        """
        self.combo_tags_type.config(state="normal")
        self.gender_combo.config(state="normal")
        self.combo_number.config(state="normal")
        
         # Disable irrelevant comboboxes for names
        self.combo_mode.config(state="disabled")
        self.combo_pronoun_case.config(state="disabled")
        self.combo_form_preposition.config(state="disabled")
        self.combo_grade_tags.config(state="disabled")
        self.combo_time.config(state="disabled")
        self.combo_person.config(state="disabled")

    def enable_comboboxes_Verbs(self):
        """
        Enables the combo boxes relevant to verbs and disables irrelevant combo boxes.
        """
        self.combo_tags_type.config(state="normal")
        self.combo_mode.config(state="normal")
        self.combo_time.config(state="normal") 
        self.combo_person.config(state="normal")
        self.combo_number.config(state="normal")
        self.gender_combo.config(state="normal")

         # Disable irrelevant comboboxes for verbs
        self.combo_pronoun_case.config(state="disabled")
        self.combo_form_preposition.config(state="disabled")
        self.combo_grade_tags.config(state="disabled")

    def enable_comboboxes_Pronouns(self):
        """
        Enables the combo boxes relevant to pronouns and disables irrelevant combo boxes.
        """
        self.combo_tags_type.config(state="normal")
        self.combo_person.config(state="normal")
        self.gender_combo.config(state="normal")
        self.combo_number.config(state="normal")
        self.combo_pronoun_case.config(state="normal")
        
        # Disable irrelevant comboboxes for pronouns
        self.combo_mode.config(state="disabled")
        self.combo_form_preposition.config(state="disabled")
        self.combo_grade_tags.config(state="disabled")
        self.combo_time.config(state="disabled")

    def enable_comboboxes_Conjunctions(self):
        """
        Enables the combo boxes relevant to conjunctions and disables irrelevant combo boxes.
        """
        self.combo_tags_type.config(state="normal")
        
        # Disable irrelevant comboboxes for conjunctions
        self.combo_mode.config(state="disabled")
        self.combo_pronoun_case.config(state="disabled")
        self.combo_form_preposition.config(state="disabled")
        self.combo_grade_tags.config(state="disabled")
        self.combo_time.config(state="disabled")
        self.combo_person.config(state="disabled")
        self.gender_combo.config(state="disabled")
        self.combo_number.config(state="disabled")

    def enable_comboboxes_Numerals(self):
        """
        Enables the combo boxes relevant to numerals and disables irrelevant combo boxes.
        """
        self.combo_tags_type.config(state="normal")
        self.gender_combo.config(state="normal")
        self.combo_number.config(state="normal")
        
        # Disable irrelevant comboboxes for numerals
        self.combo_mode.config(state="disabled")
        self.combo_pronoun_case.config(state="disabled")
        self.combo_form_preposition.config(state="disabled")
        self.combo_grade_tags.config(state="disabled")
        self.combo_time.config(state="disabled")
        self.combo_person.config(state="disabled")
    
    def enable_comboboxes_Prepositions(self):
        """
        Enables the combo boxes relevant to prepositions and disables irrelevant combo boxes.
        """
        self.combo_tags_type.config(state="normal")
        self.combo_form_preposition.config(state="normal")
        self.gender_combo.config(state="normal")
        self.combo_number.config(state="normal")
        
        # Disable irrelevant comboboxes for prepositions
        self.combo_mode.config(state="disabled")
        self.combo_pronoun_case.config(state="disabled")
        self.combo_grade_tags.config(state="disabled")
        self.combo_time.config(state="disabled")
        self.combo_person.config(state="disabled")

    def enable_comboboxes(self,event):
        """
        Enables the appropriate comboboxes based on the selected tag from the combobox.

        Parameters:
        event (Event): The event that triggers the function call.

        Returns:
        None
        """
        self.selected_tag = self.combo_tags.get()
        # Enable the appropriate comboboxes based on the selected tag
        if self.selected_tag == "ADJETIVOS":
            self.enable_comboboxes_Adjectives()
        if(self.selected_tag=="ADVERBIOS"):
            self.enable_comboboxes_Adverbs()
        if(self.selected_tag=="ARTÍCULOS"):
            self.enable_comboboxes_Articles()
        if(self.selected_tag=="ARTÍCULOS"):
            self.enable_comboboxes_Determinants()
        if(self.selected_tag=="NOMBRES"):
            self.enable_comboboxes_Names()
        if(self.selected_tag=="VERBOS"):
            self.enable_comboboxes_Verbs()
        if(self.selected_tag=="PRONOMBRES"):
            self.enable_comboboxes_Pronouns()
        if(self.selected_tag=="CONJUNCIONES"):
            self.enable_comboboxes_Conjunctions()
        if(self.selected_tag=="NUMERALES"):
            self.enable_comboboxes_Numerals()
        if(self.selected_tag=="PREPOSICIONES"):
            self.enable_comboboxes_Prepositions()
    
    def count_sentences(self,file):
        """
        Counts the number of sentences in a given file.

        Parameters:
        file (str): The path to the file.

        Returns:
        int: The number of sentences in the file.
        """
        content=self.getFileContent(file)
        # Split the content by newline to get individual sentences
        sentences = content.split('\n')
        # Strip whitespace and filter out empty sentences
        sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
        # Return the count of sentences
        return len(sentences)
        
    def getFileContent(self,name):
        """
        Retrieves the content of a file.

        Parameters:
        name (str): The name or path of the file.

        Returns:
        str: The content of the file.
        """
        self.filename=open(name, "r", encoding="utf-8")
        self.filecontent=self.filename.read()
        self.filename.close()
        return self.filecontent

    def openFile(self):
        """
        Opens a file dialog to select an input file and displays the selected file's name.

        Returns:
        None
        """
        self.nameFileInput=fd.askopenfilename(initialdir = "/",title = "Select an intput file",filetypes = (("Text files","*.txt"),("All files","*.*")))
        if self.nameFileInput!='':
            # Enable the delete button and display the selected file's name
            self.buttonborrarpathinput.config(state="normal")
            print(self.nameFileInput)
            os.path.basename(self.nameFileInput)
            self.labelpathinput.config(text=f"{os.path.basename(self.nameFileInput)}")
        else:
             # Show a warning if no file is selected
            mb.showwarning("Information", "Please, Choose your file")

    def DeleteFileInput(self):
        """
        Clears the input file selection.

        Returns:
        None
        """
        if self.nameFileInput!='':
            self.labelpathinput.config(text="")
            self.nameFileInput=""
            self.buttonborrarpathinput.config(state="disabled")

    def saveFile(self):
        """
        Opens a file dialog to select an output file and displays the selected file's name.

        Returns:
        None
        """
        self.nameFileOuPut=fd.asksaveasfilename(initialdir = "/",title = "Select an output file",filetypes = (("Text files","*.txt"),("All files","*.*")))
        if self.nameFileOuPut!='':
            # Enable the delete button and display the selected file's name
            self.buttonborrarpathout.config(state="normal")
            self.labelpathoutput.config(text=f"{os.path.basename(self.nameFileOuPut)}")
        else:
            # Show a warning if no file is selected
            mb.showwarning("Information", "Please, Choose your file.")

    def DeleteFileOut(self):
        """
        Clears the output file selection.

        Returns:
        None
        """
        if self.nameFileOuPut!='':
            self.labelpathoutput.config(text="")
            self.nameFileOuPut=""
            self.buttonborrarpathout.config(state="disabled")
    
    def GetMessages(self,newvalue):
        """
        Creates a message for the OpenAI API request.

        Parameters:
        newvalue (str): The content to be sent to the API.

        Returns:
        list: A list containing the message as a dictionary.
        """
        self.message= [{
                        "role": "user", 
                        "content": newvalue
                        }]
        return self.message
    
    def GetReponseGPT(self,chatgptPrompt):
        """
        Gets the response from the OpenAI API based on the provided prompt.

        Parameters:
        chatgptPrompt (str): The prompt to be sent to the API.

        Returns:
        str: The response from the OpenAI API.
        """
        msg=self.GetMessages(chatgptPrompt)
        try:
            chat_completion = self.client.chat.completions.create(
                model=self.modelname,
                messages=msg
                )
            
            self.responseGPT=chat_completion.choices[0].message.content
            self.strMessage='Ok'
        except OpenAIError as ai_err:
            # Show a warning if there's an error
            self.ai_response_msg_processing_Exception = ai_err.body["message"]
            mb.showwarning("Information",self.ai_response_msg_processing_Exception)
        return  self.responseGPT
    
    def taggerFile(self):
        """
        Tags the content of the selected input file and writes the result to the selected output file.

        Returns:
        None
        """
        if self.nameFileOuPut!='' and self.nameFileInput!='':
             # Get the content of the input file
            self.filecontent=self.getFileContent(self.nameFileInput)
            number_sentences = self.count_sentences(self.nameFileInput)
            if number_sentences<26:
                # Create the prompt for tagging
                self.chatgptPrompt='''Etiqueta el texto que se encuentra en medio de <> segun el grupo EAGLES. Se deben etiquetar todas las palabras y signos de puntuación.
                    Despues genera un formato de salida como este palabra#Pos tagg donde palabra es la palabra a etiquetar y pos tagg es la etiqueta asignada. 
                    Se debe generar una palabra por linea con su etiqueta como el siguiente ejemplo: 
                    Los#DA0MP0 
                    niños#NCMP000
                    comen#VMIP3P0 
                    helado#VMP00SM
                    .#Fp'''+'<'+self.filecontent+'>'
                self.responseTagg=self.GetReponseGPT(self.chatgptPrompt)
                with open(self.nameFileOuPut, 'w', encoding='utf-8') as output_file:
                    # Write the response to the output file
                    output_file.write(str(self.responseTagg))

                # Enable relevant widgets and update the scrolled text widget with the response
                self.combo_tags.config(state="normal")
                self.textbox_selected_text.config(state="normal")
                self.scrolledtext1.delete("1.0", tk.END)  
                self.scrolledtext1.insert("1.0", self.responseTagg)
                self.filecontentOutput=self.getFileContent(self.nameFileOuPut)

                # Append the response to the output file if it is not empty
                if os.stat(self.nameFileOuPut).st_size != 0:
                    with open(self.nameFileOuPut, 'a', encoding='utf-8') as output_file:
                        output_file.write('\n'+str(self.responseTagg))
            else:
                    # Show a warning if the number of sentences exceeds the limit
                    mb.showwarning("Information",f"The total number of sentences allowed is 25")
        else:
            # Show a warning if either input or output file is not selected
            mb.showwarning("Information", "First, select an Input or Output corpus.")
        
root=TaggingFiles()