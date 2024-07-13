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
    
    def __init__(self):
        self.window=tk.Tk()
        self.client = OpenAI(api_key=os.environ.get("KEYGPT"))
        self.filenamePreproces=""
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
        # Lista de etiquetas POS
        self.POS_tags = [
            "ADJETIVOS", "ADVERBIOS", "ARTÍCULOS", "DETERMINANTES", "NOMBRES",
            "VERBOS", "PRONOMBRES", "CONJUNCIONES", "NUMERALES", "INTERJECCIONES",
            "ABREVIATURAS", "PREPOSICIONES", "SIGNOS DE PUNTUACIÓN"
        ]
        self.POS_tags_mapping = {
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
        # Lista de etiquetas adicionales
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
        self.additional_tags = {
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
        }

        # Lista de géneros
        self.genders = [
            "Masculino M",
            "Femenino F",
            "Común C"
        ]
        self.genres_mapping = {
            "M":{"Generos","Masculino M"},
            "F":{"Generos","Femenino F"},
            "C":{"Generos","Común C"}
            }

        # Lista de modos
        self.modes = [
            "Indicativo I",
            "Subjuntivo S",
            "Imperativo M",
            "Condicional C",
            "Infinitivo N",
            "Gerundio G",
            "Participio P"
        ]
        self.mapping_modes = {
           "I":{"Modos","Indicativo I"},
           "S":{"Modos","Subjuntivo S"},
           "M":{"Modos","Imperativo M"},
           "C":{"Modos","Condicional C"},
           "N":{"Modos","Infinitivo N"},
           "G":{"Modos","Gerundio G"},
           "P":{"Modos","Participio P"}
        }
        # Lista de números
        self.numbers = [
            "Singular S",
            "Plural P"
        ]
        self.mapping_numbers = {
            "S":{"Numeros","Singular S"},
            "P":{"Numeros","Plural P"}
            }
        # Lista de tiempos
        self.times = [
            "Presente P",
            "Imperfecto I",
            "Futuro F",
            "Pasado S"
        ]
        self.mapping_times = {
            "P":{"Tiempos","Presente P"  },  
            "I":{"Tiempos","Imperfecto I"},
            "F":{"Tiempos","Futuro F"    },
            "S":{"Tiempos","Pasado S"    }
            }
        # Lista de personas
        self.people = [
            "Primera 1",
            "Segunda 2",
            "Tercera 3"
        ]
        self.people_mapping = {
            "1":{"Personas","Primera 1"},
            "2":{"Personas","Segunda 2"},
            "3":{"Personas","Tercera 3"}
            }
        # Lista de formas de preposición
        self.preposition_forms = [
            "Simple S",
            "Contraída C"
        ]
        self.forms_preposition_mapping = {
           "S":{"Formas","Simple S"},
           "C":{"Formas","Contraída C"}
        }
        self.PronounsCase=["Nominativo N", 
                             "Acusativo A", 
                             "Dativo D", 
                             "Oblicuo O"
        ]
        self.PronounsCase_mapping={
            "N":{"PronombreCaso","Nominativo N"},
            "A":{"PronombreCaso","Acusativo A"},
            "D":{"PronombreCaso","Dativo D"},
            "O":{"PronombreCaso","Oblicuo O"}
        }
                          
        self.GetFiles()     
        self.GetFrameCorpus()
        self.GetFrameTagg()    
        self.window.mainloop()
    
    def set_selection(self,mapping,etiqueta):
        selection = {}
        for caracter, opciones in mapping.items():
            if caracter in etiqueta:
                selection.update(opciones)
        return selection
        
    def set_comboboxes(self,etiqueta):
        if etiqueta[0] =="N":
            self.selection= self.set_selection(self.POS_tags_mapping,etiqueta)

        self.combo_tags.set(self.selection.get("Categoria", ""))
        self.combo_tags.set(self.selection.get("Generos", ""))
        self.combo_tags.set(self.selection.get("Modos", ""))
        self.combo_tags.set(self.selection.get("Numero", ""))
        self.combo_tags.set(self.selection.get("Tiempos", ""))
        self.combo_tags.set(self.selection.get("Personas", ""))
        self.combo_tags.set(self.selection.get("Formas", ""))
        self.combo_tags.set(self.selection.get("PronombreCaso", ""))
    
    def GetFiles(self):
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

        self.label3=self.label2=tk.Label(self.labelframefiles,text="Press on button AI Tagger to start+",font=self.font1)
        self.label3.grid(row=4, column=0, columnspan=3, pady=2)

        self.button1=tk.Button(self.labelframefiles, font=self.font1, bg="green", fg="white", text=" AI Tagger", command=self.taggerFile)
        self.button1.grid(row=5, column=0, columnspan=3, pady=20)

    def GetFrameCorpus(self):
        self.labelframecorpus=ttk.LabelFrame(self.window, text="Pos Tagging")        
        self.labelframecorpus.grid(row=0, column=1, padx=2, pady=2)

        self.labeltitle=tk.Label(self.labelframecorpus,text="Pos tagging results",font=self.font1)
        self.labeltitle.grid(row=0, column=1, columnspan=3, pady=2)
        
        self.scrolledtext1=st.ScrolledText(self.labelframecorpus,font=self.font1)
        # Vincular el evento de clic con la función para capturar la selección
        self.scrolledtext1.bind("<ButtonRelease-1>", self.select_tagg)
        self.scrolledtext1.grid(row=1, column=1, columnspan=3, padx=2, pady=2)
        
    def GetFrameTagg(self):

        self.labelframetagg=ttk.LabelFrame(self.window, text="Tag Modification")        
        self.labelframetagg.grid(row=2, column=0, padx=2, pady=2)
        ##1
        # Agrega un ComboBox y rellénalo con las etiquetas POS
        self.labeltitle=tk.Label(self.labelframetagg,text="Choose Category",font=self.font1)
        self.labeltitle.grid(row=3, column=0, padx=2, pady=2)
        self.combo_tags = ttk.Combobox( self.labelframetagg, values=self.POS_tags)
        self.combo_tags.grid(row=3, column=1, padx=2, pady=2)

        # Agrega un ComboBox adicional con etiquetas específicas
        self.labeltitle=tk.Label(self.labelframetagg,text="Choose a Type",font=self.font1)
        self.labeltitle.grid(row=4, column=0, padx=2, pady=2)
        self.combo_tags_type = ttk.Combobox(self.labelframetagg, values=self.additional_tags)
        self.combo_tags_type.grid(row=4, column=1, padx=2, pady=2)
        ##1
        ##2
        # Agrega otro ComboBox con etiquetas adicionales
        self.labeltitle=tk.Label(self.labelframetagg,text="Choose a Degree",font=self.font1)
        self.labeltitle.grid(row=5, column=0, padx=2, pady=2)
        self.combo_grade_tags = ttk.Combobox(self.labelframetagg, values=["Apreciativo"])
        self.combo_grade_tags.grid(row=5, column=1, padx=2, pady=2)
        # Agrega un ComboBox para género
        self.labeltitle=tk.Label(self.labelframetagg,text="Choose a Gender",font=self.font1)
        self.labeltitle.grid(row=6, column=0, padx=2, pady=2)
        self.gender_combo = ttk.Combobox(self.labelframetagg, values=self.genders)
        self.gender_combo.grid(row=6, column=1, padx=2, pady=2)
        ##2
        ##3
        # Agrega un ComboBox para modo
        self.labeltitle=tk.Label(self.labelframetagg,text="Choose a Mode",font=self.font1)
        self.labeltitle.grid(row=7, column=0, padx=2, pady=2)
        self.combo_mode = ttk.Combobox(self.labelframetagg, values=self.modes)
        self.combo_mode.grid(row=7, column=1, padx=2, pady=2)
        # Agrega un ComboBox para número
        self.labeltitle=tk.Label(self.labelframetagg,text="Choose a Number",font=self.font1)
        self.labeltitle.grid(row=3, column=2, padx=2, pady=2)
        self.combo_number = ttk.Combobox(self.labelframetagg, values=self.numbers)
        self.combo_number.grid(row=3, column=3, padx=2, pady=2)
        ##2
        ##3
        # Agrega un ComboBox para times
        self.labeltitle=tk.Label(self.labelframetagg,text="Choose Verbal Tense",font=self.font1)
        self.labeltitle.grid(row=4, column=2, padx=2, pady=2)
        self.combo_time = ttk.Combobox(self.labelframetagg, values=self.times)
        self.combo_time.grid(row=4, column=3, padx=2, pady=2)

        # Agrega un ComboBox para persona
        self.labeltitle=tk.Label(self.labelframetagg,text="Choose a Person",font=self.font1)
        self.labeltitle.grid(row=5, column=2, padx=2, pady=2)
        self.combo_person = ttk.Combobox(self.labelframetagg, values=self.people)
        self.combo_person.grid(row=5, column=3, padx=2, pady=2)
        ##2
        ##3
        # Agrega un ComboBox para la forma de la preposición
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
        # Vincular el evento de cambio de selección del ComboBox combo_etiquetas
        self.combo_tags.bind("<<ComboboxSelected>>", self.enable_comboboxes)

    def SaveFrame(self):
       
        self.labelframeSaveTagg=ttk.LabelFrame(self.window, text="Save tags")        
        self.labelframeSaveTagg.grid(row=2, column=1, padx=2, pady=2)
                # Agrega un TextBox para mostrar el texto seleccionado
        self.labeltitle=tk.Label(self.labelframeSaveTagg,text="Modify your tag and save",font=self.font1)
        self.labeltitle.grid(row=3, column=1, padx=2, pady=2,columnspan=3)
       
        self.selected_text = tk.StringVar()
        self.textbox_selected_text = tk.Entry(self.labelframeSaveTagg, textvariable=self.selected_text, state="readonly",font=self.font1)
        self.textbox_selected_text.grid(row=4, column=1, padx=2, pady=2, columnspan=3)

        # Agrega botones para guardar etiqueta y agregar al diccionario
        self.labeltitle=tk.Label(self.labelframeSaveTagg,text="Press on button for save",font=self.font1)
        self.labeltitle.grid(row=5, column=1, padx=2, pady=2) #columnspan=4
       
        self.boton_save_tag = tk.Button(self.labelframeSaveTagg, text="Save Tag",bg="blue", fg="white",font=self.font1,  command=self.save_tag)
        self.boton_save_tag.grid(row=5, column=2, padx=2, pady=2)
       
        self.boton_agregar_diccionario = tk.Button(self.labelframeSaveTagg, text="Save to dictionary",font=self.font1, bg="blue", fg="white", command=self.add_to_dictionary)
        self.boton_agregar_diccionario.grid(row=5, column=3, padx=2, pady=2)

    def add_to_dictionary():
        pass
    
    def save_tag():
        pass

    def select_tagg(self,event):
        self.seleccion = self.scrolledtext1.tag_ranges(tk.SEL)
        if self.seleccion:
            self.textbox_selected_text.config(state="normal")
            self.selected_tag = self.scrolledtext1.get(*self.scrolledtext1.tag_ranges(tk.SEL))
            etiqueta=self.selected_tag.split("#")
            self.set_comboboxes(str(etiqueta[1]))
            self.selected_text.set(self.selected_tag)

    def enable_comboboxes_Adjectives(self):
        self.combo_tags_type.config(state="normal")
        self.combo_grade_tags.config(state="normal")
        self.gender_combo.config(state="normal")
        self.combo_number.config(state="normal")
        #DESABILITADO
        self.combo_mode.config(state="disabled")
        self.combo_pronoun_case.config(state="disabled")
        self.combo_form_preposition.config(state="disabled")
        self.combo_time.config(state="disabled")
        
    def enable_comboboxes_Adverbs(self):
        self.combo_tags_type.config(state="normal")
        #DESABILITADO
        self.combo_mode.config(state="disabled")
        self.combo_pronoun_case.config(state="disabled")
        self.combo_form_preposition.config(state="disabled")
        self.combo_grade_tags.config(state="disabled")
        self.gender_combo.config(state="disabled")
        self.combo_number.config(state="disabled")
        self.combo_time.config(state="disabled")

    def enable_comboboxes_Articles(self):
        self.combo_tags_type.config(state="normal")
        self.gender_combo.config(state="normal")
        self.combo_number.config(state="normal")
        #DESABILITADO
        self.combo_mode.config(state="disabled")
        self.combo_pronoun_case.config(state="disabled")
        self.combo_form_preposition.config(state="disabled")
        self.combo_grade_tags.config(state="disabled")
        self.combo_person.config(state="disabled")
        self.combo_time.config(state="disabled")

    def enable_comboboxes_Determinants(self):
        self.combo_tags_type.config(state="normal")
        self.combo_person.config(state="normal")
        self.gender_combo.config(state="normal")
        self.combo_number.config(state="normal")
        #DESABILITADO
        self.combo_mode.config(state="disabled")
        self.combo_pronoun_case.config(state="disabled")
        self.combo_form_preposition.config(state="disabled")
        self.combo_grade_tags.config(state="disabled")
        self.combo_time.config(state="disabled")

    def enable_comboboxes_Names(self):
        self.combo_tags_type.config(state="normal")
        self.gender_combo.config(state="normal")
        self.combo_number.config(state="normal")
        #DESABILITADO
        self.combo_mode.config(state="disabled")
        self.combo_pronoun_case.config(state="disabled")
        self.combo_form_preposition.config(state="disabled")
        self.combo_grade_tags.config(state="disabled")
        self.combo_time.config(state="disabled")
        self.combo_person.config(state="disabled")

    def enable_comboboxes_Verbs(self):
        self.combo_tags_type.config(state="normal")
        self.combo_mode.config(state="normal")
        self.combo_time.config(state="normal") 
        self.combo_person.config(state="normal")
        self.combo_number.config(state="normal")
        self.gender_combo.config(state="normal")
         #DESABILITADO
       # self.combo_mode.config(state="disabled")
        self.combo_pronoun_case.config(state="disabled")
        self.combo_form_preposition.config(state="disabled")
        self.combo_grade_tags.config(state="disabled")

    def enable_comboboxes_Pronouns(self):
        self.combo_tags_type.config(state="normal")
        self.combo_person.config(state="normal")
        self.gender_combo.config(state="normal")
        self.combo_number.config(state="normal")
        self.combo_pronoun_case.config(state="normal")
        #DESABILITADO
        self.combo_mode.config(state="disabled")
        self.combo_form_preposition.config(state="disabled")
        self.combo_grade_tags.config(state="disabled")
        self.combo_time.config(state="disabled")

    def enable_comboboxes_Conjunctions(self):
        self.combo_tags_type.config(state="normal")
        #DESABILITADO
        self.combo_mode.config(state="disabled")
        self.combo_pronoun_case.config(state="disabled")
        self.combo_form_preposition.config(state="disabled")
        self.combo_grade_tags.config(state="disabled")
        self.combo_time.config(state="disabled")
        self.combo_person.config(state="disabled")
        self.gender_combo.config(state="disabled")
        self.combo_number.config(state="disabled")

    def enable_comboboxes_Numerals(self):
        self.combo_tags_type.config(state="normal")
        self.gender_combo.config(state="normal")
        self.combo_number.config(state="normal")
        #DESABILITADO
        self.combo_mode.config(state="disabled")
        self.combo_pronoun_case.config(state="disabled")
        self.combo_form_preposition.config(state="disabled")
        self.combo_grade_tags.config(state="disabled")
        self.combo_time.config(state="disabled")
        self.combo_person.config(state="disabled")
    
    def enable_comboboxes_Prepositions(self):
        self.combo_tags_type.config(state="normal")
        self.combo_form_preposition.config(state="normal")
        self.gender_combo.config(state="normal")
        self.combo_number.config(state="normal")
        #DESABILITADO
        self.combo_mode.config(state="disabled")
        self.combo_pronoun_case.config(state="disabled")
        self.combo_grade_tags.config(state="disabled")
        self.combo_time.config(state="disabled")
        self.combo_person.config(state="disabled")

    def enable_comboboxes(self,event):
        self.selected_tag = self.combo_tags.get()
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
            content=self.getFileContent(file)
            sentences = content.split('\n')
            sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
            return len(sentences)
        
    def getFileContent(self,name):
        self.filename=open(name, "r", encoding="utf-8")
        self.filecontent=self.filename.read()
        self.filename.close()
        return self.filecontent

    def openFile(self):
        self.nameFileInput=fd.askopenfilename(initialdir = "/",title = "Select an intput file",filetypes = (("Text files","*.txt"),("All files","*.*")))
        if self.nameFileInput!='':
            self.buttonborrarpathinput.config(state="normal")
            print(self.nameFileInput)
            os.path.basename(self.nameFileInput)
            self.labelpathinput.config(text=f"{os.path.basename(self.nameFileInput)}")
        else:
            mb.showwarning("Information", "Please, Choose your file")

    def DeleteFileInput(self):
        if self.nameFileInput!='':
            self.labelpathinput.config(text="")
            self.nameFileInput=""
            self.buttonborrarpathinput.config(state="disabled")

    def saveFile(self):
        self.nameFileOuPut=fd.asksaveasfilename(initialdir = "/",title = "Select an output file",filetypes = (("Text files","*.txt"),("All files","*.*")))
        if self.nameFileOuPut!='':
            self.buttonborrarpathout.config(state="normal")
            self.labelpathoutput.config(text=f"{os.path.basename(self.nameFileOuPut)}")
        else:
            mb.showwarning("Information", "Please, Choose your file.")

    def DeleteFileOut(self):
        if self.nameFileOuPut!='':
            self.labelpathoutput.config(text="")
            self.nameFileOuPut=""
            self.buttonborrarpathout.config(state="disabled")
    
    def GetMessages(self,newvalue):
        self.message= [{
                        "role": "user", 
                        "content": newvalue
                        }]
        return self.message
    
    def GetReponseGPT(self,chatgptPrompt):
        msg=self.GetMessages(chatgptPrompt)
        try:
            chat_completion = self.client.chat.completions.create(
                model=self.modelname,
                messages=msg
                )
            
            self.responseGPT=chat_completion.choices[0].message.content
            self.strMessage='Ok'
        except OpenAIError as ai_err:
            self.ai_response_msg_processing_Exception = ai_err.body["message"]
            mb.showwarning("Information",self.ai_response_msg_processing_Exception)
        return  self.responseGPT
    
    def taggerFile(self):
        if self.nameFileOuPut!='' and self.nameFileInput!='':
            self.filecontent=self.getFileContent(self.nameFileInput)
            number_sentences = self.count_sentences(self.nameFileInput)
            if number_sentences<26:
                
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
                    output_file.write(str(self.responseTagg))
                    ##COMBO Y SCROOLLED
                self.combo_tags.config(state="normal")
                self.textbox_selected_text.config(state="normal")
                self.scrolledtext1.delete("1.0", tk.END)  
                self.scrolledtext1.insert("1.0", self.responseTagg)
                self.filecontentOutput=self.getFileContent(self.nameFileOuPut)

                if os.stat(self.nameFileOuPut).st_size != 0:
                    with open(self.nameFileOuPut, 'a', encoding='utf-8') as output_file:
                        output_file.write('\n'+str(self.responseTagg))
            else:
                    mb.showwarning("Information",f"The total number of sentences allowed is 25")
        else:
            mb.showwarning("Information", "First, select an Input or Output corpus.")
        
    def SaveTagg(self,tagg):
        pass
        #La salida seria en formato Json. Aqui se guarda la etiqueta en el archivo de salida en formato json
        # en su token correspondiente del texto etiquetado, 
        #despues de modificarla en la interfaz.
    
    def SaveDictionary(self,word,tagg):
        pass
        #Aqui se guarda aquellas etiquetas de tokens que son repetitivas, como articulos y adverbios. 
        #Se guardan en el arhivo de diccionario y además se guarda en el archivo json de salida.
        #TaggDict = dict()

app1=TaggingFiles()