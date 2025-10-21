import fs from 'fs'
import path from 'path'
import { fileURLToPath } from 'url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))

// Criar um ícone PNG simples de 16x16 (pixel art do Digimundo)
const trayIconData = Buffer.from([
  0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A, // PNG signature
  0x00, 0x00, 0x00, 0x0D, 0x49, 0x48, 0x44, 0x52, // IHDR chunk
  0x00, 0x00, 0x00, 0x10, 0x00, 0x00, 0x00, 0x10, // 16x16
  0x08, 0x02, 0x00, 0x00, 0x00, 0x90, 0x91, 0x68, 0x36, // bit depth, color type, etc
  0x00, 0x00, 0x00, 0x3C, 0x49, 0x44, 0x41, 0x54, // IDAT chunk (simplified)
  0x28, 0x91, 0x63, 0x60, 0x18, 0x05, 0xA3, 0x80, 
  0x91, 0x81, 0x81, 0x81, 0x41, 0x16, 0x0C, 0x32,
  0x30, 0x30, 0x88, 0x05, 0x43, 0x0C, 0x0C, 0x0C,
  0x62, 0xC1, 0x10, 0x03, 0x03, 0x83, 0x58, 0x30,
  0xC4, 0xC0, 0xC0, 0x20, 0x16, 0x0C, 0x31, 0x30,
  0x30, 0x88, 0x05, 0x43, 0x0C, 0x0C, 0x0C, 0x62,
  0x00, 0x00, 0x0F, 0x8C, 0x02, 0x61, 0x50, 0x67,
  0xA9, 0x3B,
  0x00, 0x00, 0x00, 0x00, 0x49, 0x45, 0x4E, 0x44, // IEND chunk
  0xAE, 0x42, 0x60, 0x82
])

// Criar um ícone maior 64x64 em base64
const mainIconBase64 = `iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAAACXBIWXMAAAsTAAALEwEAmpwYAAAEaklEQVR4nO2bW2wUVRjHf2d2d9vutrS0pS1FLhVQBEQFRYkXvEQT45MmJr74oA8+mPjggy8+GB988MEnH3zwQROjMTEmGiMaE40XvF8QRQWVIiItLdCWXtrdbWd3Zs7xnN3OzM7szOzObLe1zC/5Jzsz55zv+3/nnO98l1lQUFBQUFBQUFBQUFBQUFAog2AwGFBVVVVVVQUg5HI5M5PJmGa+ykAoFPIpimJkMhlDluUcUNVUQQv4/X69oaGhqaOjo729vb25ra2tuampqaGhoSEQDAb9Pp/PpyiKAhiGgWEY5HI5I5PJmMlkMjU6OjoyPDw8NDAw0N/X13dqYGBgwDTNKuBWnhYVtYDP52toamrq6O7uXrZixYplS5YsWdDW1tZaV1dXG4lEav1+f8Bp5LIs67lcThcURcFQFAxNw9R1UJQiOVmW5Ww8Hh8bGRkZ6e3tPXH48OGjvb29J+Px+KgzqJZtS0tLS2dnZ+fClStXXrp27drLFy5cuKC1tbXFF0j/gSwKI21VINEUkRMEQRAURVE1TZNVVZVHR0fH+/r6Tvf09Bw6ePDggd7e3pOGYZwBFACmp6dn3YYNG266/vrrr1+0aNGiaDQaDYZCIb/TGGUG9IyOmc3IVAY9paGnJPSkhJ7QgAmCTxAEv08QBJ+IoAgCAEY2h5nNlhzfNE3I5XKZTCYT7+vrO7F3794v9+3b991oNDpq1Z+RuHjx4u4NGzZsvP7665cvX768u7m5uam2tjaiRaNE2hqItDUS7ojia/D7BFUQZMNFCLrhJvMb8jBFiqRF5i/UM02TXC6Xy2QymeHh4cFDhw79snPnzg/379//E3DWZ5rmsvXr19+3ZcuWu9euXbvK7/f7K1lhCRLomhlG5xhZdCOHrtlFNQzXxWk1JiYmJg8cOPDTe++99+mPP/74dU1NzaWbN2++b+vWrVvXrVu3ShAEoc7qoKeY7hKYnJycPHHixB/vvPPOh59//vnn4XD4ws2bN9+/devWratXr15RtRYXOoZhGJlMZvzYsWO/7dixY/vOnTv3tre3z9+0adND9913360LFy5sr7YUkwFFURTFMAxtfHz81JEjRw6+8847Hx84cOAb3TCMeZ2dnRs3bNhwz9q1a1dEo9HGautLxQqYpklJk1YdAJOTk9OxWOzsL7/8cuitt97a8eOPP+6vrq42VqxYccWdd955x7Jly5bW19fX+Xy+mi7d0PiJBJOTU9On//l7qP/Q4WPHjx37PZlMjgCzQVdcRxAEQRAEQfD5fJrP5/MJQt4WLJ6dzxlsGQZYhVfALnqhbYHqN7L5Ag0ePz8cRhGRhWKnqgA2qqqqQkEzMGAqpJLJ5MzJyUkdqCvJu8Qs7Q6LxWJpYFr2eDOzFCbmFcLkyWQymclkssDcJU4IglBDIZlDKezxhXP5FvQsJk1EliQzk83mjGw2a5qm6eNS+ZdQiMGvJhYJBGsiUe+dJJwlWSg6S5G0fRWOOZ4Kg4CyJP8HRFz7zl3OfwG0iJM0CHzkkgAAAABJRU5ErkJggg==`

// Salvar os ícones
fs.writeFileSync(
  path.join(__dirname, 'tray-icon.png'),
  trayIconData
)

fs.writeFileSync(
  path.join(__dirname, 'digimundo-icon.png'),
  Buffer.from(mainIconBase64, 'base64')
)

// console.log('✅ Ícones criados com sucesso!')