import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from PIL import Image, ImageTk  # pip install Pillow
import urllib.request
import io

# ============================================================
# BASE DE DATOS DE PERFUMES ORIGINALES
# ============================================================
PERFUMES = [
    {
        "id": 1,
        "nombre": "Chanel N°5",
        "marca": "Chanel",
        "tipo": "Mujer",
        "familia": "Floral Aldehído",
        "precio": 150.00,
        "ml": 100,
        "descripcion": "Un clásico atemporal creado en 1921. Notas de salida de aldehídos, ylang-ylang y neroli. Corazón de rosa de mayo y jazmín. Fondo de sándalo y vainilla.",
        "img": "https://images.unsplash.com/photo-1541643600914-78b084683601?w=300"
    },
    {
        "id": 2,
        "nombre": "Dior Sauvage",
        "marca": "Dior",
        "tipo": "Hombre",
        "familia": "Amaderado Especiado",
        "precio": 130.00,
        "ml": 100,
        "descripcion": "Frescura audaz con bergamota de Calabria y pimienta. Corazón de lavanda y geranio. Fondo de ambroxan y cedro. Un ícono moderno de la perfumería masculina.",
        "img": "https://images.unsplash.com/photo-1594035910387-fea47794261f?w=300"
    },
    {
        "id": 3,
        "nombre": "J'adore",
        "marca": "Dior",
        "tipo": "Mujer",
        "familia": "Floral Frutal",
        "precio": 145.00,
        "ml": 100,
        "descripcion": "Un bouquet floral luminoso. Notas de pera y melón, corazón de jazmín, rosa y ylang-ylang. Fondo de almizcle y vainilla.",
        "img": "https://images.unsplash.com/photo-1588405748880-12d1d2a59f75?w=300"
    },
    {
        "id": 4,
        "nombre": "Bleu de Chanel",
        "marca": "Chanel",
        "tipo": "Hombre",
        "familia": "Amaderado Aromático",
        "precio": 140.00,
        "ml": 100,
        "descripcion": "Libertad y determinación en un frasco. Cítricos frescos, menta y pomelo. Corazón de jazmín y nuez moscada. Fondo de sándalo, cedro e incienso.",
        "img": "https://images.unsplash.com/photo-1523293182086-7651a899d37f?w=300"
    },
    {
        "id": 5,
        "nombre": "La Vie Est Belle",
        "marca": "Lancôme",
        "tipo": "Mujer",
        "familia": "Oriental Gourmand",
        "precio": 125.00,
        "ml": 75,
        "descripcion": "La felicidad embotellada. Iris y pachulí con notas gourmand de praliné, vainilla y pachulí. Una fragancia dulce y adictiva.",
        "img": "https://images.unsplash.com/photo-1592945403244-b3fbafd7f539?w=300"
    },
    {
        "id": 6,
        "nombre": "Acqua di Giò",
        "marca": "Giorgio Armani",
        "tipo": "Hombre",
        "familia": "Acuático Cítrico",
        "precio": 110.00,
        "ml": 100,
        "descripcion": "Inspirada en la isla de Pantelleria. Notas marinas, limón y bergamota. Corazón de jazmín y romero. Fondo de almizcle blanco y cedro.",
        "img": "https://images.unsplash.com/photo-1587017539504-67cfbddac569?w=300"
    },
    {
        "id": 7,
        "nombre": "Coco Mademoiselle",
        "marca": "Chanel",
        "tipo": "Mujer",
        "familia": "Oriental Floral",
        "precio": 155.00,
        "ml": 100,
        "descripcion": "Una fragancia fresca y sensual. Naranja y bergamota, corazón de rosa y jazmín, fondo de pachulí, vetiver y vainilla blanca.",
        "img": "https://images.unsplash.com/photo-1563170351-be82bc888aa4?w=300"
    },
    {
        "id": 8,
        "nombre": "1 Million",
        "marca": "Paco Rabanne",
        "tipo": "Hombre",
        "familia": "Especiado Cuero",
        "precio": 105.00,
        "ml": 100,
        "descripcion": "Audaz y magnético. Pomelo, menta y mandarina. Corazón de rosa, canela y especias. Fondo de cuero, ámbar y pachulí.",
        "img": "https://images.unsplash.com/photo-1615634260167-c8cdede054de?w=300"
    },
]

# ============================================================
# CLASE PRINCIPAL DE LA APLICACIÓN
# ============================================================
class CatalogoPerfumes:
    def __init__(self, root):
        self.root = root
        self.root.title("✨ Catálogo de Perfumes Originales ✨")
        self.root.geometry("1100x700")
        self.root.configure(bg="#f5e6d3")
        
        # Variables de filtro
        self.filtro_tipo = tk.StringVar(value="Todos")
        self.filtro_marca = tk.StringVar(value="Todas")
        self.busqueda = tk.StringVar()
        
        self.crear_encabezado()
        self.crear_filtros()
        self.crear_grid_perfumes()
        self.crear_pie()
        
        self.mostrar_perfumes()
    
    def crear_encabezado(self):
        header = tk.Frame(self.root, bg="#8b4513", height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(
            header, text="PERFUMES ORIGINALES",
            font=("Georgia", 24, "bold"),
            bg="#8b4513", fg="#f5e6d3"
        ).pack(pady=20)
    
    def crear_filtros(self):
        frame_filtros = tk.Frame(self.root, bg="#f5e6d3")
        frame_filtros.pack(fill=tk.X, padx=20, pady=10)
        
        # Búsqueda
        tk.Label(frame_filtros, text="🔍 Buscar:", bg="#f5e6d3",
                 font=("Arial", 11, "bold")).grid(row=0, column=0, padx=5)
        entry_buscar = tk.Entry(frame_filtros, textvariable=self.busqueda,
                                font=("Arial", 11), width=25)
        entry_buscar.grid(row=0, column=1, padx=5)
        entry_buscar.bind("<KeyRelease>", lambda e: self.mostrar_perfumes())
        
        # Filtro por tipo
        tk.Label(frame_filtros, text="Tipo:", bg="#f5e6d3",
                 font=("Arial", 11, "bold")).grid(row=0, column=2, padx=15)
        tipos = ["Todos", "Mujer", "Hombre"]
        combo_tipo = ttk.Combobox(frame_filtros, textvariable=self.filtro_tipo,
                                  values=tipos, state="readonly", width=12)
        combo_tipo.grid(row=0, column=3)
        combo_tipo.bind("<<ComboboxSelected>>", lambda e: self.mostrar_perfumes())
        
        # Filtro por marca
        marcas = ["Todas"] + sorted(list(set(p["marca"] for p in PERFUMES)))
        tk.Label(frame_filtros, text="Marca:", bg="#f5e6d3",
                 font=("Arial", 11, "bold")).grid(row=0, column=4, padx=15)
        combo_marca = ttk.Combobox(frame_filtros, textvariable=self.filtro_marca,
                                   values=marcas, state="readonly", width=15)
        combo_marca.grid(row=0, column=5)
        combo_marca.bind("<<ComboboxSelected>>", lambda e: self.mostrar_perfumes())
    
    def crear_grid_perfumes(self):
        # Canvas con scrollbar
        container = tk.Frame(self.root, bg="#f5e6d3")
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.canvas = tk.Canvas(container, bg="#f5e6d3", highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#f5e6d3")
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Permitir scroll con rueda del mouse
        self.canvas.bind_all("<MouseWheel>",
                             lambda e: self.canvas.yview_scroll(-1*(e.delta//120), "units"))
    
    def cargar_imagen(self, url, size=(180, 180)):
        """Descarga y redimensiona una imagen desde URL"""
        try:
            with urllib.request.urlopen(url, timeout=3) as response:
                data = response.read()
            img = Image.open(io.BytesIO(data))
            img = img.resize(size, Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(img)
        except Exception as e:
            # Placeholder si falla la carga
            img = Image.new("RGB", size, "#d4a574")
            return ImageTk.PhotoImage(img)
    
    def mostrar_perfumes(self):
        # Limpiar grid anterior
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # Aplicar filtros
        perfumes_filtrados = []
        busq = self.busqueda.get().lower()
        for p in PERFUMES:
            if self.filtro_tipo.get() != "Todos" and p["tipo"] != self.filtro_tipo.get():
                continue
            if self.filtro_marca.get() != "Todas" and p["marca"] != self.filtro_marca.get():
                continue
            if busq and busq not in p["nombre"].lower() and busq not in p["marca"].lower():
                continue
            perfumes_filtrados.append(p)
        
        if not perfumes_filtrados:
            tk.Label(self.scrollable_frame, text="No se encontraron perfumes.",
                     bg="#f5e6d3", font=("Arial", 12)).pack(pady=40)
            return
        
        # Crear tarjetas en grid (4 columnas)
        columnas = 4
        for idx, perfume in enumerate(perfumes_filtrados):
            fila, col = divmod(idx, columnas)
            self.crear_tarjeta(perfume, fila, col)
    
    def crear_tarjeta(self, perfume, fila, col):
        tarjeta = tk.Frame(self.scrollable_frame, bg="white",
                          relief="raised", bd=2, padx=10, pady=10)
        tarjeta.grid(row=fila, column=col, padx=10, pady=10, sticky="n")
        
        # Imagen
        img = self.cargar_imagen(perfume["img"])
        label_img = tk.Label(tarjeta, image=img, bg="white")
        label_img.image = img  # Mantener referencia
        label_img.pack(pady=5)
        
        # Nombre
        tk.Label(tarjeta, text=perfume["nombre"],
                 font=("Georgia", 13, "bold"), bg="white",
                 fg="#8b4513", wraplength=180).pack()
        
        # Marca
        tk.Label(tarjeta, text=perfume["marca"],
                 font=("Arial", 10, "italic"), bg="white",
                 fg="#666").pack()
        
        # Tipo y ml
        tk.Label(tarjeta, text=f"{perfume['tipo']} • {perfume['ml']}ml",
                 font=("Arial", 9), bg="white", fg="#888").pack()
        
        # Precio
        tk.Label(tarjeta, text=f"${perfume['precio']:.2f}",
                 font=("Arial", 14, "bold"), bg="white",
                 fg="#2e7d32").pack(pady=5)
        
        # Botón ver detalles
        btn = tk.Button(tarjeta, text="Ver Detalles",
                       bg="#8b4513", fg="white",
                       font=("Arial", 10, "bold"),
                       relief="flat", cursor="hand2",
                       command=lambda p=perfume: self.ver_detalles(p))
        btn.pack(pady=5, fill="x")
    
    def ver_detalles(self, perfume):
        """Ventana con detalles completos del perfume"""
        detalle = tk.Toplevel(self.root)
        detalle.title(perfume["nombre"])
        detalle.geometry("600x500")
        detalle.configure(bg="#f5e6d3")
        detalle.grab_set()
        
        # Imagen grande
        img = self.cargar_imagen(perfume["img"], (250, 250))
        lbl_img = tk.Label(detalle, image=img, bg="#f5e6d3")
        lbl_img.image = img
        lbl_img.pack(pady=15)
        
        # Información
        tk.Label(detalle, text=perfume["nombre"],
                 font=("Georgia", 22, "bold"),
                 bg="#f5e6d3", fg="#8b4513").pack()
        
        tk.Label(detalle, text=f"{perfume['marca']} • {perfume['tipo']}",
                 font=("Arial", 12, "italic"),
                 bg="#f5e6d3", fg="#555").pack()
        
        tk.Label(detalle, text=f"Familia olfativa: {perfume['familia']}",
                 font=("Arial", 11), bg="#f5e6d3").pack(pady=5)
        
        tk.Label(detalle, text=f"Volumen: {perfume['ml']} ml",
                 font=("Arial", 11), bg="#f5e6d3").pack()
        
        # Descripción
        tk.Label(detalle, text="Descripción:",
                 font=("Arial", 11, "bold"),
                 bg="#f5e6d3", fg="#8b4513").pack(pady=(10, 2))
        
        text_desc = scrolledtext.ScrolledText(detalle, height=5, width=60,
                                              font=("Arial", 10), wrap="word")
        text_desc.insert("1.0", perfume["descripcion"])
        text_desc.configure(state="disabled")
        text_desc.pack(pady=5, padx=20)
        
        # Precio y botón comprar
        tk.Label(detalle, text=f"PRECIO: ${perfume['precio']:.2f}",
                 font=("Arial", 18, "bold"),
                 bg="#f5e6d3", fg="#2e7d32").pack(pady=10)
        
        tk.Button(detalle, text="🛒 Agregar al Carrito",
                 bg="#2e7d32", fg="white",
                 font=("Arial", 12, "bold"),
                 relief="flat", cursor="hand2", padx=20, pady=8,
                 command=lambda: self.agregar_carrito(perfume, detalle)).pack(pady=5)
        
        tk.Button(detalle, text="Cerrar",
                 bg="#8b4513", fg="white",
                 font=("Arial", 10),
                 relief="flat", cursor="hand2",
                 command=detalle.destroy).pack(pady=10)
    
    def agregar_carrito(self, perfume, ventana):
        messagebox.showinfo("✅ Agregado",
                           f"'{perfume['nombre']}' agregado al carrito.\nPrecio: ${perfume['precio']:.2f}")
        ventana.destroy()
    
    def crear_pie(self):
        pie = tk.Frame(self.root, bg="#8b4513", height=40)
        pie.pack(fill=tk.X, side="bottom")
        pie.pack_propagate(False)
        tk.Label(pie, text="© 2025 Perfumes Originales - Todos los productos son 100% auténticos",
                 bg="#8b4513", fg="#f5e6d3",
                 font=("Arial", 9)).pack(pady=10)


# ============================================================
# EJECUTAR APLICACIÓN
# ============================================================
if __name__ == "__main__":
    root = tk.Tk()
    app = CatalogoPerfumes(root)
    root.mainloop()