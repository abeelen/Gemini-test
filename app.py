import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import sys

# Détection automatique de l'environnement (Streamlit vs Exécution Standard)
RUNNING_IN_STREAMLIT = "streamlit" in sys.argv or any("streamlit" in arg for arg in sys.argv)

if RUNNING_IN_STREAMLIT:
    import streamlit as st


class Ray:
    def __init__(self, x, y, vx, vy, color="orange"):
        self.pos = np.array([x, y], dtype=float)
        magnitude = np.hypot(vx, vy)
        self.dir = np.array([vx / magnitude, vy / magnitude], dtype=float)
        self.path_x = [float(x)]
        self.path_y = [float(y)]
        self.color = color


class OpticalElement:
    def __init__(self, center_x, center_y, length, angle_deg, name="Element"):
        self.center = np.array([center_x, center_y], dtype=float)
        self.length = length
        self.angle = np.radians(angle_deg)
        self.name = name
        self.tangent = np.array([np.cos(self.angle), np.sin(self.angle)])
        self.normal = np.array([-np.sin(self.angle), np.cos(self.angle)])
        self.p1 = self.center - (self.length / 2) * self.tangent
        self.p2 = self.center + (self.length / 2) * self.tangent

    def intersect(self, ray):
        v1 = ray.pos - self.p1
        v2 = self.p2 - self.p1
        perpendicular = np.array([-ray.dir[1], ray.dir[0]])
        denominator = np.dot(v2, perpendicular)
        if abs(denominator) < 1e-8:
            return None
        distance = np.cross(v2, v1) / denominator
        position = np.dot(v1, perpendicular) / denominator
        if distance > 1e-4 and 0.0 <= position <= 1.0:
            return distance
        return None


class Mirror(OpticalElement):
    def __init__(self, center_x, center_y, length, angle_deg, name="Miroir"):
        super().__init__(center_x, center_y, length, angle_deg, name)
        self.color = "crimson"

    def interact(self, ray, hit_point):
        normal = self.normal
        if np.dot(ray.dir, normal) > 0:
            normal = -normal
        ray.dir = ray.dir - 2 * np.dot(ray.dir, normal) * normal
        ray.pos = hit_point


class ThinLens(OpticalElement):
    def __init__(self, center_x, center_y, length, angle_deg, f_distance, name="Lentille"):
        super().__init__(center_x, center_y, length, angle_deg, name)
        self.f = f_distance
        self.color = "dodgerblue" if f_distance > 0 else "indigo"

    def interact(self, ray, hit_point):
        height = np.dot(hit_point - self.center, self.tangent)
        tangent_component = np.dot(ray.dir, self.tangent)
        normal_component = np.dot(ray.dir, self.normal)
        tangent_component -= height / self.f * np.sign(normal_component)
        new_dir = tangent_component * self.tangent + normal_component * self.normal
        ray.dir = new_dir / np.linalg.norm(new_dir)
        ray.pos = hit_point


class Screen(OpticalElement):
    def __init__(self, center_x, center_y, length, angle_deg, name="Écran / Détecteur"):
        super().__init__(center_x, center_y, length, angle_deg, name)
        self.color = "black"

    def interact(self, ray, hit_point):
        ray.pos = hit_point


class Scene:
    def __init__(self, title):
        self.elements = []
        self.rays = []
        self.title = title

    def add(self, item):
        if isinstance(item, OpticalElement):
            self.elements.append(item)
        elif isinstance(item, Ray):
            self.rays.append(item)

    def run(self, max_interactions=6, ext_dist=12.0):
        for ray in self.rays:
            for _ in range(max_interactions):
                closest_t, closest_el = float("inf"), None
                for element in self.elements:
                    distance = element.intersect(ray)
                    if distance is not None and distance < closest_t:
                        closest_t, closest_el = distance, element
                if closest_el is None:
                    end_pos = ray.pos + ray.dir * ext_dist
                    ray.path_x.append(float(end_pos[0]))
                    ray.path_y.append(float(end_pos[1]))
                    break
                hit_point = ray.pos + closest_t * ray.dir
                closest_el.interact(ray, hit_point)
                ray.path_x.append(float(ray.pos[0]))
                ray.path_y.append(float(ray.pos[1]))
                if isinstance(closest_el, Screen):
                    break

    def generate_animation(self, num_frames=100):
        fig, ax = plt.subplots(figsize=(10, 5))
        for element in self.elements:
            ax.plot(
                [element.p1[0], element.p2[0]],
                [element.p1[1], element.p2[1]],
                color=element.color,
                lw=3,
                label=element.name,
            )
        lines = [ax.plot([], [], color=ray.color, lw=1.5, alpha=0.8)[0] for ray in self.rays]
        animated_paths = []
        for ray in self.rays:
            total_x, total_y = [], []
            for index in range(len(ray.path_x) - 1):
                x1, x2 = ray.path_x[index], ray.path_x[index + 1]
                y1, y2 = ray.path_y[index], ray.path_y[index + 1]
                steps = max(2, int(np.hypot(x2 - x1, y2 - y1) * 20))
                total_x.extend(np.linspace(x1, x2, steps)[:-1])
                total_y.extend(np.linspace(y1, y2, steps)[:-1])
            total_x.append(ray.path_x[-1])
            total_y.append(ray.path_y[-1])
            animated_paths.append((total_x, total_y))

        def init():
            for line in lines:
                line.set_data([], [])
            return lines

        def update(frame):
            for index, line in enumerate(lines):
                x_data, y_data = animated_paths[index]
                path_index = min(int((frame / num_frames) * len(x_data)), len(x_data))
                line.set_data(x_data[:path_index], y_data[:path_index])
            return lines

        handles, labels = ax.get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        ax.set_title(self.title, fontsize=11, weight="bold")
        ax.axis("equal")
        ax.grid(True, alpha=0.2)
        ax.legend(by_label.values(), by_label.keys(), loc="upper left", fontsize=8)
        all_x = [element.p1[0] for element in self.elements] + [element.p2[0] for element in self.elements]
        all_y = [element.p1[1] for element in self.elements] + [element.p2[1] for element in self.elements]
        ax.set_xlim(min(all_x) - 3, max(all_x) + 5)
        ax.set_ylim(min(all_y) - 3, max(all_y) + 3)
        ani = animation.FuncAnimation(
            fig, update, frames=num_frames + 1, init_func=init, blit=True, interval=20, repeat=True
        )
        return fig, ani

    def show_native(self):
        fig, ani = self.generate_animation()
        plt.show()

    def show_in_streamlit(self):
        fig, ani = self.generate_animation()
        st.components.v1.html(ani.to_jshtml(), height=550, scrolling=False)
        plt.close(fig)


def build_scene(type_scene, custom_params=None):
    params = custom_params or {}
    if type_scene == "1. Lentille Unique (Focalisation)":
        scene = Scene("Exemple 1 : Focalisation par un dioptre convergent")
        focal_length = params.get("f_val", 3.0)
        scene.add(ThinLens(0, 0, 3.0, 90, focal_length, "Lentille Mince"))
        scene.add(Screen(focal_length, 0, 2.0, 90, "Foyer Image / Capteur"))
        for y in np.linspace(-1.0, 1.0, 7):
            scene.add(Ray(-4, y, 1, 0, "dodgerblue"))
    elif type_scene == "2. Système à deux lentilles (Collimation)":
        scene = Scene("Exemple 2 : Collimateur de faisceau divergent")
        f1, f2 = params.get("f1", 1.5), params.get("f2", 3.0)
        scene.add(ThinLens(0, 0, 2.0, 90, f1, "Lentille Divergente L1"))
        scene.add(ThinLens(4.0, 0, 3.0, 90, f2, "Lentille Convergente L2"))
        for angle in np.linspace(-0.2, 0.2, 6):
            scene.add(Ray(-1.5, 0, np.cos(angle), np.sin(angle), "crimson"))
    elif type_scene == "3. Miroir Plan incliné (Déviation)":
        scene = Scene("Exemple 3 : Déviation angulaire d'un faisceau par un miroir")
        angle = params.get("angle", 45)
        scene.add(Mirror(0, 0, 2.5, angle, f"Miroir à {angle}°"))
        scene.add(Screen(0, 3.0, 2.0, 0, "Plan d'Analyse"))
        for y in np.linspace(-0.4, 0.4, 5):
            scene.add(Ray(-3, y, 1, 0, "darkorange"))
    elif type_scene == "4. Réflexion et Focalisation Combinée":
        scene = Scene("Exemple 4 : Déviation angulaire et refocusing")
        mirror_angle, focal_length = params.get("angle_m", 45), params.get("f_lens", 2.0)
        scene.add(Mirror(0, 0, 2.0, mirror_angle, "Miroir de Renvoi"))
        scene.add(ThinLens(0, 2.0, 2.0, 0, focal_length, "Lentille de Focalisation"))
        scene.add(Screen(0, 2.0 + focal_length, 1.5, 0, "Capteur CCD"))
        for y in np.linspace(-0.3, 0.3, 5):
            scene.add(Ray(-3, y, 1, 0, "forestgreen"))
    else:
        raise ValueError(f"Scène inconnue : {type_scene}")
    scene.run()
    return scene


if __name__ == "__main__" and RUNNING_IN_STREAMLIT:
    examples = [
        "1. Lentille Unique (Focalisation)",
        "2. Système à deux lentilles (Collimation)",
        "3. Miroir Plan incliné (Déviation)",
        "4. Réflexion et Focalisation Combinée",
    ]
    st.set_page_config(page_title="Simulation Geometrical Optics", layout="wide")
    st.title("Exemples Adaptés du Dépôt `geometrical_optics`")
