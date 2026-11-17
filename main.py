import json
import os
import random
import tkinter as tk
from tkinter import messagebox, scrolledtext

class ProgrammingQuiz:
    def __init__(self, root, filename="questions.json"):
        """
        Constructor de la clase principal. Inicializa los atributos del juego,
        carga las preguntas y construye la interfaz gráfica.
        """
        self.root = root
        self.filename = filename
        self.score = 0
        self.lives = 3
        self.current_index = 0
        self.selected_questions = []
        
        # Carga las preguntas y valida que existan antes de iniciar
        self.questions = self.load_questions()
        if self.questions:
            self.initialize_game()
            self.create_main_window()

    # ==========================================
    # PARTE 1: Carga y validación del archivo JSON
    # ==========================================
    def load_questions(self):
        """
        Carga las preguntas desde un archivo JSON.
        Verifica si el archivo existe y asegura que contenga al menos 5 preguntas,
        utilizando manejo de excepciones con try/except.
        """
        # Verifica si el archivo existe para prevenir errores fatales
        if not os.path.exists(self.filename):
            messagebox.showerror("Error", f"El archivo {self.filename} no existe.")
            return []

        try:
            # Abre y lee el archivo JSON de forma segura
            with open(self.filename, "r", encoding="utf-8") as file:
                questions = json.load(file)
                
                # Valida el requisito de la rúbrica (mínimo 5 preguntas)
                if len(questions) < 5:
                    messagebox.showerror("Error", "El archivo debe contener al menos 5 preguntas.")
                    return []
                    
                return questions
                
        except json.JSONDecodeError:
            messagebox.showerror("Error", "El archivo JSON está mal formateado.")
            return []

    # ==========================================
    # PARTE 2: Lógica del juego y selección aleatoria
    # ==========================================
    def initialize_game(self):
        """
        Selecciona aleatoriamente 5 preguntas de la lista total 
        y restablece los contadores del juego.
        """
        # Selecciona 5 preguntas al azar usando random.sample
        self.selected_questions = random.sample(self.questions, 5)
        self.current_index = 0
        self.score = 0
        self.lives = 3

    def check_answer(self, user_answer):
        """
        Verifica si la respuesta ingresada por el usuario es correcta.
        Actualiza el puntaje o las vidas y avanza al siguiente índice.
        """
        current_q = self.selected_questions[self.current_index]
        
        # Compara la respuesta ignorando espacios y mayúsculas/minúsculas
        if user_answer.strip().lower() == current_q["answer"].strip().lower():
            self.score += 10  # Suma puntos si acierta
            result = True
        else:
            self.lives -= 1   # Resta una vida si falla
            result = False
            
        # Incrementa el índice para pasar a la siguiente pregunta
        self.current_index += 1
        return result

    # ==========================================
    # PARTE 3: Interfaz Gráfica Principal
    # ==========================================
    def create_main_window(self):
        """
        Configura la ventana principal de la aplicación, la barra de menú
        y los widgets de la interfaz gráfica requeridos por la rúbrica.
        """
        self.root.title("Programming Fundamentals Quiz")
        self.root.geometry("600x480")
        
        # --- 1. Barra de Menú (Uso de Menu widget) ---
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)
        
        # Opción Archivo (File)
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Add Question", command=self.open_add_question_window)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Opción Ayuda (Help)
        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)
        self.help_menu.add_command(label="About", command=self.show_about)
        
        # --- 2. ScrolledText para las preguntas (Fuente Times New Roman obligatoria) ---
        self.question_text = scrolledtext.ScrolledText(
            self.root, 
            wrap=tk.WORD, 
            width=65, 
            height=8,
            font=("Times New Roman", 12)
        )
        self.question_text.pack(pady=15)
        self.question_text.config(state=tk.DISABLED) # Bloqueado para lectura exclusiva
        
        # --- 3. Entry para la respuesta del usuario ---
        self.answer_label = tk.Label(self.root, text="Your Answer:", font=("Arial", 10))
        self.answer_label.pack()
        
        self.answer_entry = tk.Entry(self.root, width=40, font=("Arial", 11))
        self.answer_entry.pack(pady=5)
        
        # --- 4. Botón de envío ---
        self.submit_button = tk.Button(
            self.root, 
            text="Submit Answer", 
            command=self.handle_answer_submission,
            bg="#4CAF50",
            fg="white"
        )
        self.submit_button.pack(pady=10)
        
        # --- 5. Etiquetas de Estado (Vidas y Puntaje) ---
        self.status_label = tk.Label(
            self.root, 
            text=f"Lives: {self.lives} | Score: {self.score}", 
            font=("Arial", 11, "bold")
        )
        self.status_label.pack(pady=10)
        
        # Muestra la primera pregunta en pantalla
        self.display_current_question()

    def display_current_question(self):
        """
        Muestra la pregunta actual dentro del widget ScrolledText.
        """
        if self.current_index < len(self.selected_questions):
            q_data = self.selected_questions[self.current_index]["question"]
            
            self.question_text.config(state=tk.NORMAL)
            self.question_text.delete("1.0", tk.END)
            self.question_text.insert(tk.END, f"Question {self.current_index + 1}:\n\n{q_data}")
            self.question_text.config(state=tk.DISABLED)
            
            self.answer_entry.delete(0, tk.END)
        else:
            self.show_game_over()

    def handle_answer_submission(self):
        """
        Maneja el evento del botón de envío, valida la respuesta
        y actualiza la interfaz o el estado del juego.
        """
        user_input = self.answer_entry.get()
        if not user_input.strip():
            messagebox.showwarning("Warning", "Please enter an answer.")
            return
            
        is_correct = self.check_answer(user_input)
        
        if is_correct:
            messagebox.showinfo("Correct!", "Great job! That's the correct answer.")
        else:
            messagebox.showerror("Incorrect", "Wrong answer. You lost a life.")
            
        self.status_label.config(text=f"Lives: {self.lives} | Score: {self.score}")
        
        if self.lives <= 0:
            self.show_game_over()
        else:
            self.display_current_question()

    def show_game_over(self):
        """
        Muestra la pantalla de resultados finales al terminar el juego.
        """
        messagebox.showinfo("Game Over", f"Quiz finished!\nFinal Score: {self.score}")
        self.root.quit()

    def show_about(self):
        """
        Muestra información del proyecto en la opción de ayuda.
        """
        messagebox.showinfo("About", "Programming Fundamentals Quiz\nBuilt with Python & Tkinter")

    # ==========================================
    # PARTE 4: Ventana Secundaria (Toplevel) para Agregar Preguntas
    # ==========================================
    def open_add_question_window(self):
        """
        Abre una ventana Toplevel para permitir al usuario registrar una nueva pregunta
        y guardarla automáticamente en el archivo JSON.
        """
        self.top = tk.Toplevel(self.root)
        self.top.title("Add New Question")
        self.top.geometry("400x300")
        
        # Campo para la pregunta
        tk.Label(self.top, text="New Question:", font=("Arial", 10)).pack(pady=5)
        self.new_q_entry = tk.Entry(self.top, width=45, font=("Arial", 10))
        self.new_q_entry.pack(pady=5)
        
        # Campo para la respuesta
        tk.Label(self.top, text="Answer:", font=("Arial", 10)).pack(pady=5)
        self.new_a_entry = tk.Entry(self.top, width=45, font=("Arial", 10))
        self.new_a_entry.pack(pady=5)
        
        # Botón para guardar
        save_button = tk.Button(
            self.top, 
            text="Save Question", 
            command=self.save_new_question,
            bg="#2196F3",
            fg="white"
        )
        save_button.pack(pady=20)

    def save_new_question(self):
        """
        Lee los campos de texto, agrega la nueva pregunta al archivo JSON
        y cierra la ventana secundaria.
        """
        new_q = self.new_q_entry.get().strip()
        new_a = self.new_a_entry.get().strip()
        
        if not new_q or not new_a:
            messagebox.showwarning("Warning", "All fields must be filled.", parent=self.top)
            return
            
        new_entry = {
            "question": new_q,
            "answer": new_a
        }
        
        try:
            # Añade la pregunta a la lista en memoria y actualiza el archivo JSON
            self.questions.append(new_entry)
            with open(self.filename, "w", encoding="utf-8") as file:
                json.dump(self.questions, file, indent=4, ensure_ascii=False)
                
            messagebox.showinfo("Success", "Question added successfully!", parent=self.top)
            self.top.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Could not save file: {e}", parent=self.top)

# Bloque de ejecución principal
if __name__ == "__main__":
    root = tk.Tk()
    app = ProgrammingQuiz(root)
    root.mainloop()             