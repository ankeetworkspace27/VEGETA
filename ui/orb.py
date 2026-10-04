from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import (
    QColor,
    QPainter,
    QPainterPath,
    QPen,
    QRadialGradient,
)
from PySide6.QtWidgets import QPushButton

import math


class AIOrb(QPushButton):

    def __init__(self):
        super().__init__()

        self.setFixedSize(260, 260)

        # ---------------------------------------------------------
        # BUTTON
        # ---------------------------------------------------------

        self.setFlat(True)
        self.setFocusPolicy(Qt.NoFocus)
        self.setCursor(Qt.PointingHandCursor)

        self.setStyleSheet("""
            QPushButton {
                border: none;
                background: transparent;
                padding: 0px;
            }

            QPushButton:hover {
                background: transparent;
            }

            QPushButton:pressed {
                background: transparent;
            }
        """)

        self.on_orb_click = None

        # ---------------------------------------------------------
        # STATE
        # ---------------------------------------------------------

        self.state = "idle"

        # ---------------------------------------------------------
        # ANIMATION
        # ---------------------------------------------------------

        self.phase = 0.0

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate)
        self.timer.start(16)

        self.clicked.connect(self.handle_click)

    # =============================================================
    # STATE
    # =============================================================

    def set_state(self, state):

        if not state:
            return

        state = str(state).lower().strip()

        valid_states = (
            "idle",
            "listening",
            "thinking",
            "speaking",
        )

        if state not in valid_states:
            state = "idle"

        if self.state == state:
            return

        self.state = state

        print(
            f"VEGETA ORB: State -> {self.state.upper()}"
        )

        self.update()

    # =============================================================
    # CLICK
    # =============================================================

    def handle_click(self):

        print("VEGETA ORB CLICKED")

        if self.on_orb_click is not None:

            print("ORB -> HOME")

            self.on_orb_click()

        else:

            print(
                "ERROR: No HomeWindow callback connected"
            )

    # =============================================================
    # ANIMATION
    # =============================================================

    def animate(self):

        # State-specific movement.
        #
        # Idle:
        #     slow and calm
        #
        # Listening:
        #     more responsive
        #
        # Thinking:
        #     fastest ribbon movement
        #
        # Speaking:
        #     smooth medium pulse

        animation_speed = {
            "idle": 0.018,
            "listening": 0.027,
            "thinking": 0.034,
            "speaking": 0.025,
        }.get(
            self.state,
            0.018
        )

        self.phase += animation_speed

        if self.phase >= math.tau:
            self.phase -= math.tau

        self.update()

    # =============================================================
    # PAINT
    # =============================================================

    def paintEvent(self, event):

        painter = QPainter(self)

        painter.setRenderHint(
            QPainter.Antialiasing
        )

        painter.setRenderHint(
            QPainter.SmoothPixmapTransform
        )

        cx = self.width() / 2
        cy = self.height() / 2

        # ---------------------------------------------------------
        # STATE PARAMETERS
        # ---------------------------------------------------------

        state_parameters = {

            "idle": {
                "breathing": 1.00,
                "bloom": 1.00,
                "core": 1.00,
            },

            "listening": {
                "breathing": 1.18,
                "bloom": 1.10,
                "core": 1.08,
            },

            "thinking": {
                "breathing": 1.08,
                "bloom": 1.05,
                "core": 1.04,
            },

            "speaking": {
                "breathing": 1.22,
                "bloom": 1.13,
                "core": 1.10,
            },

        }

        parameters = state_parameters.get(
            self.state,
            state_parameters["idle"]
        )

        # ---------------------------------------------------------
        # BREATHING
        # ---------------------------------------------------------

        breathing = (
            math.sin(
                self.phase * 1.25
            ) + 1.0
        ) / 2.0

        breathing *= parameters["breathing"]

        # Keep the overall size almost identical.
        scale = (
            1.0
            + breathing * 0.045
        )

        # ---------------------------------------------------------
        # BLOOM
        # ---------------------------------------------------------

        bloom_radius = (
            88
            + breathing * 12 * parameters["bloom"]
        )

        bloom = QRadialGradient(
            cx,
            cy,
            bloom_radius
        )

        bloom.setColorAt(
            0.0,
            QColor(
                40,
                225,
                255,
                55 + int(
                    breathing * 25
                )
            )
        )

        bloom.setColorAt(
            0.35,
            QColor(
                0,
                180,
                255,
                30
            )
        )

        bloom.setColorAt(
            0.7,
            QColor(
                70,
                80,
                255,
                12
            )
        )

        bloom.setColorAt(
            1.0,
            QColor(
                0,
                0,
                0,
                0
            )
        )

        painter.setPen(
            Qt.NoPen
        )

        painter.setBrush(
            bloom
        )

        painter.drawEllipse(
            int(cx - bloom_radius),
            int(cy - bloom_radius),
            int(bloom_radius * 2),
            int(bloom_radius * 2)
        )

        # ---------------------------------------------------------
        # RIBBONS
        # ---------------------------------------------------------

        painter.save()

        painter.translate(
            cx,
            cy
        )

        painter.scale(
            scale,
            scale
        )

        self.draw_ribbon(
            painter,
            70,
            12,
            self.phase * 0.8,
            QColor(
                0,
                225,
                255,
                190
            ),
            QColor(
                70,
                120,
                255,
                110
            )
        )

        self.draw_ribbon(
            painter,
            63,
            10,
            -self.phase * 1.15 + 1.8,
            QColor(
                40,
                255,
                220,
                130
            ),
            QColor(
                0,
                180,
                255,
                150
            )
        )

        self.draw_ribbon(
            painter,
            57,
            9,
            self.phase * 1.4 + 3.0,
            QColor(
                120,
                80,
                255,
                130
            ),
            QColor(
                0,
                220,
                255,
                150
            )
        )

        self.draw_ribbon(
            painter,
            75,
            7,
            -self.phase * 0.65 + 4.2,
            QColor(
                0,
                255,
                255,
                100
            ),
            QColor(
                100,
                80,
                255,
                80
            )
        )

        painter.restore()

        # ---------------------------------------------------------
        # CORE
        # ---------------------------------------------------------

        core_radius = (
            42
            + breathing
            * 5
            * parameters["core"]
        )

        core = QRadialGradient(
            cx - 8,
            cy - 10,
            core_radius
        )

        core.setColorAt(
            0.0,
            QColor(
                235,
                255,
                255,
                180
            )
        )

        core.setColorAt(
            0.18,
            QColor(
                150,
                250,
                255,
                150
            )
        )

        core.setColorAt(
            0.45,
            QColor(
                20,
                210,
                255,
                90
            )
        )

        core.setColorAt(
            0.75,
            QColor(
                30,
                120,
                255,
                30
            )
        )

        core.setColorAt(
            1.0,
            QColor(
                0,
                0,
                0,
                0
            )
        )

        painter.setBrush(
            core
        )

        painter.setPen(
            Qt.NoPen
        )

        painter.drawEllipse(
            int(cx - core_radius),
            int(cy - core_radius),
            int(core_radius * 2),
            int(core_radius * 2)
        )

        # ---------------------------------------------------------
        # MOVING HIGHLIGHT
        # ---------------------------------------------------------

        highlight_speed = {
            "idle": 1.0,
            "listening": 1.15,
            "thinking": 1.30,
            "speaking": 1.10,
        }.get(
            self.state,
            1.0
        )

        highlight_x = (
            cx
            + math.sin(
                self.phase
                * 1.3
                * highlight_speed
            ) * 20
        )

        highlight_y = (
            cy
            + math.cos(
                self.phase
                * 1.1
                * highlight_speed
            ) * 15
        )

        highlight = QRadialGradient(
            highlight_x,
            highlight_y,
            25
        )

        highlight.setColorAt(
            0.0,
            QColor(
                255,
                255,
                255,
                120
            )
        )

        highlight.setColorAt(
            0.35,
            QColor(
                220,
                255,
                255,
                60
            )
        )

        highlight.setColorAt(
            1.0,
            QColor(
                255,
                255,
                255,
                0
            )
        )

        painter.setBrush(
            highlight
        )

        painter.drawEllipse(
            int(highlight_x - 25),
            int(highlight_y - 25),
            50,
            50
        )

        painter.end()

    # =============================================================
    # RIBBON
    # =============================================================

    def draw_ribbon(
        self,
        painter,
        radius,
        width,
        rotation,
        color1,
        color2
    ):

        path = QPainterPath()

        points = 90

        for i in range(
            points + 1
        ):

            t = i / points

            angle = (
                rotation
                + t * math.tau
            )

            wave = (
                math.sin(
                    angle * 2.0
                    + self.phase * 1.7
                ) * 7
            )

            wave += (
                math.sin(
                    angle * 3.0
                    - self.phase * 1.2
                ) * 3
            )

            r = (
                radius
                + wave
            )

            x = (
                math.cos(angle)
                * r
            )

            y = (
                math.sin(angle)
                * r
            )

            if i == 0:

                path.moveTo(
                    x,
                    y
                )

            else:

                path.lineTo(
                    x,
                    y
                )

        # ---------------------------------------------------------
        # MAIN RIBBON
        # ---------------------------------------------------------

        pen = QPen(
            color1
        )

        pen.setWidthF(
            width
        )

        pen.setCapStyle(
            Qt.RoundCap
        )

        pen.setJoinStyle(
            Qt.RoundJoin
        )

        painter.setPen(
            pen
        )

        painter.setBrush(
            Qt.NoBrush
        )

        painter.drawPath(
            path
        )

        # ---------------------------------------------------------
        # INNER RIBBON
        # ---------------------------------------------------------

        inner_pen = QPen(
            color2
        )

        inner_pen.setWidthF(
            width * 0.42
        )

        inner_pen.setCapStyle(
            Qt.RoundCap
        )

        painter.setPen(
            inner_pen
        )

        painter.drawPath(
            path
        )