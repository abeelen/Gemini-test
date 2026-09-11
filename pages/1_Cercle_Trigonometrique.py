import matplotlib
import numpy as np
import streamlit as st

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from ui_theme import apply_amns_theme

st.set_page_config(page_title="Cercle Trigonométrique", layout="centered")
apply_amns_theme()

ANGLES_CLASSIQUES = [0, 30, 45, 60, 90, 120, 135, 150, 180, 210, 225, 240, 270, 300, 315, 330, 360]


class CercleTrigonometriqueInteractif:
    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(7, 7))

        self.angles_remarquables = {
            0: "0",
            30: r"$\frac{\pi}{6}$",
            45: r"$\frac{\pi}{4}$",
            60: r"$\frac{\pi}{3}$",
            90: r"$\frac{\pi}{2}$",
            120: r"$\frac{2\pi}{3}$",
            135: r"$\frac{3\pi}{4}$",
            150: r"$\frac{5\pi}{6}$",
            180: r"$\pi$",
            210: r"$\frac{7\pi}{6}$",
            225: r"$\frac{5\pi}{4}$",
            240: r"$\frac{4\pi}{3}$",
            270: r"$\frac{3\pi}{2}$",
            300: r"$\frac{5\pi}{3}$",
            315: r"$\frac{7\pi}{4}$",
            330: r"$\frac{11\pi}{6}$",
            360: r"$2\pi$",
        }

        self._tracer_fond_fixe()

        self.ligne_rayon, = self.ax.plot([], [], color="red", linewidth=2.5, zorder=4)
        self.point_cercle = self.ax.scatter([], [], color="red", s=60, zorder=5)

        self.proj_x, = self.ax.plot([], [], color="blue", linestyle="--", alpha=0.7, linewidth=1.5)
        self.proj_y, = self.ax.plot([], [], color="green", linestyle="--", alpha=0.7, linewidth=1.5)

        self.txt_cos = self.ax.text(
            0, 0, "", color="blue", fontsize=10, fontweight="bold", horizontalalignment="center"
        )
        self.txt_sin = self.ax.text(
            0, 0, "", color="green", fontsize=10, fontweight="bold", verticalalignment="center"
        )

    def _tracer_fond_fixe(self):
        theta = np.linspace(0, 2 * np.pi, 300)
        self.ax.plot(np.cos(theta), np.sin(theta), color="black", linewidth=1.5)
        self.ax.axhline(0, color="black", linewidth=1.2)
        self.ax.axvline(0, color="black", linewidth=1.2)

        for deg, label in self.angles_remarquables.items():
            rad = np.radians(deg)
            x_f, y_f = np.cos(rad), np.sin(rad)
            self.ax.scatter(x_f, y_f, color="gray", s=15, alpha=0.3, zorder=3)
            self.ax.text(
                x_f * 1.14,
                y_f * 1.14,
                label,
                fontsize=10,
                color="gray",
                horizontalalignment="center",
                verticalalignment="center",
            )

        valeurs_ticks = [-1, -np.sqrt(3) / 2, -np.sqrt(2) / 2, -0.5, 0, 0.5, np.sqrt(2) / 2, np.sqrt(3) / 2, 1]
        labels_ticks = [
            r"$-1$",
            r"$-\frac{\sqrt{3}}{2}$",
            r"$-\frac{\sqrt{2}}{2}$",
            r"$-\frac{1}{2}$",
            r"$0$",
            r"$\frac{1}{2}$",
            r"$\frac{\sqrt{2}}{2}$",
            r"$\frac{\sqrt{3}}{2}$",
            r"$1$",
        ]
        self.ax.set_xticks(valeurs_ticks)
        self.ax.set_xticklabels(labels_ticks, fontsize=9, rotation=45)
        self.ax.set_yticks(valeurs_ticks)
        self.ax.set_yticklabels(labels_ticks, fontsize=9)

        self.ax.set_xlim(-1.3, 1.3)
        self.ax.set_ylim(-1.3, 1.3)
        self.ax.set_aspect("equal")
        self.ax.set_xlabel("Cosinus (x)", fontsize=11, color="blue")
        self.ax.set_ylabel("Sinus (y)", fontsize=11, color="green")
        self.ax.grid(True, which="both", linestyle=":", alpha=0.1)

    def set_angle(self, angle_deg: float):
        angle_normalise = angle_deg % 360
        rad = np.radians(angle_deg)
        x, y = np.cos(rad), np.sin(rad)

        self.ligne_rayon.set_data([0, x], [0, y])
        self.proj_x.set_data([x, x], [0, y])
        self.proj_y.set_data([0, x], [y, y])
        self.point_cercle.set_offsets([[x, y]])

        offset_x = 0.06 if y >= 0 else -0.10
        self.txt_cos.set_position((x, -offset_x))
        self.txt_cos.set_text(f"cos = {x:.2f}")

        offset_y = 0.06 if x >= 0 else -0.25
        self.txt_sin.set_position((offset_y, y))
        self.txt_sin.set_text(f"sin = {y:.2f}")

        angle_proche = min(self.angles_remarquables.keys(), key=lambda k: abs(k - angle_normalise))
        if abs(angle_normalise - angle_proche) < 1e-2:
            texte_angle = self.angles_remarquables[angle_proche]
            titre = f"Angle remarquable : {texte_angle} ({int(round(angle_normalise))}°)"
        else:
            titre = f"Angle quelconque : {angle_deg:.1f}°"

        self.ax.set_title(titre, fontsize=13, pad=15, fontweight="bold")
        return self.fig


@st.cache_resource
def initialiser_cercle():
    return CercleTrigonometriqueInteractif()


def initialiser_etat_angles():
    st.session_state.setdefault("angle_classique", 45)
    st.session_state.setdefault("angle_curseur", 45.0)


def appliquer_angle_classique():
    st.session_state["angle_curseur"] = float(st.session_state["angle_classique"])


cercle = initialiser_cercle()
initialiser_etat_angles()

st.title("📐 Cercle Trigonométrique — AMNS Physique")

st.selectbox(
    "Classical angles",
    options=ANGLES_CLASSIQUES,
    key="angle_classique",
    on_change=appliquer_angle_classique,
    help="Choisissez un angle remarquable pour positionner directement le rayon.",
)

angle_curseur = st.slider(
    "Ajuster l'angle (en degrés) :",
    min_value=0.0,
    max_value=360.0,
    step=0.5,
    key="angle_curseur",
)

figure_mise_a_jour = cercle.set_angle(angle_curseur)
st.pyplot(figure_mise_a_jour)
