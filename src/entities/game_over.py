from ..utils import GameConfig
from ..utils.machine_learning import *
from .entity import Entity
from .variables import *

class GameOver(Entity):
    def __init__(self, config: GameConfig) -> None:
        super().__init__(
            config=config,
            image=config.images.game_over,
            x=(config.window.width - config.images.game_over.get_width()) // 2,
            y=int(config.window.height * 0.2),
        )

def showGameOverScreen(crashInfo):
    """Melakukan pembaruan genetik di sini"""
    global current_pool  # Variabel global untuk memperbarui pool model.
    global fitness  # Variabel global untuk nilai kebugaran setiap model.
    global generation  # Variabel global untuk nomor generasi.
    new_weights = []  # Daftar untuk menyimpan bobot baru.
    total_fitness = 0  # Total kebugaran semua model.
    for select in range(total_models):  # Iterasi untuk setiap model.
        total_fitness += fitness[select]  # Menambahkan kebugaran model ke total_fitness.
    for select in range(total_models):  # Iterasi untuk setiap model.
        fitness[select] /= total_fitness  # Normalisasi nilai kebugaran.
        if select > 0:  # Untuk setiap model selain yang pertama.
            fitness[select] += fitness[select-1]  # Menambahkan kebugaran model sebelumnya.
    for select in range(int(total_models/2)):  # Iterasi untuk setengah jumlah model.
        parent1 = random.uniform(0, 1)  # Memilih orang tua 1 secara acak.
        parent2 = random.uniform(0, 1)  # Memilih orang tua 2 secara acak.
        idx1 = -1  # Inisialisasi indeks orang tua 1.
        idx2 = -1  # Inisialisasi indeks orang tua 2.
        for idxx in range(total_models):  # Iterasi untuk setiap model.
            if fitness[idxx] >= parent1:  # Jika kebugaran model melebihi nilai parent1.
                idx1 = idxx  # Mengatur indeks orang tua 1.
                break
        for idxx in range(total_models):  # Iterasi untuk setiap model.
            if fitness[idxx] >= parent2:  # Jika kebugaran model melebihi nilai parent2.
                idx2 = idxx  # Mengatur indeks orang tua 2.
                break
        new_weights1 = model_crossover(idx1, idx2)  # Melakukan crossover pada bobot model.
        updated_weights1 = model_mutate(new_weights1[0])  # Melakukan mutasi pada bobot model hasil crossover.
        updated_weights2 = model_mutate(new_weights1[1])  # Melakukan mutasi pada bobot model hasil crossover.
        new_weights.append(updated_weights1)  # Menambahkan bobot model baru ke daftar.
        new_weights.append(updated_weights2)  # Menambahkan bobot model baru ke daftar.
    for select in range(len(new_weights)):  # Iterasi untuk setiap model baru.
        fitness[select] = -100  # Mengatur ulang nilai kebugaran.
        current_pool[select].set_weights(new_weights[select])  # Menetapkan bobot baru untuk model.
    if save_current_pool == 1:  # Jika disetel untuk menyimpan pool saat ini.
        save_pool()  # Menyimpan pool saat ini ke file.
    generation = generation + 1  # Menambahkan nomor generasi.
    return
