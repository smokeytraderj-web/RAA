from __future__ import annotations

import sys


def main() -> int:
    try:
        from PySide6.QtWidgets import (
            QApplication,
            QComboBox,
            QFormLayout,
            QFrame,
            QHBoxLayout,
            QLabel,
            QLineEdit,
            QMainWindow,
            QPushButton,
            QTextEdit,
            QVBoxLayout,
            QWidget,
        )
    except ImportError as exc:
        raise SystemExit('Install the desktop extra: python -m pip install -e ".[desktop]"') from exc

    class Window(QMainWindow):
        def __init__(self) -> None:
            super().__init__()
            self.setWindowTitle("RAA — Research Analyst Agent")
            self.resize(980, 720)
            root = QWidget()
            layout = QVBoxLayout(root)
            brand = QLabel("GOTTFRIED & SOMBERG WEALTH MANAGEMENT")
            brand.setObjectName("brand")
            title = QLabel("Research Analyst Agent")
            title.setObjectName("title")
            subtitle = QLabel("Ask a specific investment question. RAA will build an evidence-first answer.")
            subtitle.setWordWrap(True)
            card = QFrame()
            card.setObjectName("card")
            form = QFormLayout(card)
            ticker = QLineEdit()
            ticker.setPlaceholderText("AAPL or Apple")
            horizon = QComboBox()
            horizon.addItems(["Short Term", "Medium Term", "Long Term", "All Horizons"])
            question = QTextEdit()
            question.setPlaceholderText("Example: Should we add to this position after the pullback?")
            question.setMaximumHeight(150)
            form.addRow("Security", ticker)
            form.addRow("Horizon", horizon)
            form.addRow("Question", question)
            actions = QHBoxLayout()
            actions.addStretch()
            run = QPushButton("Start Research")
            run.clicked.connect(
                lambda: status.setText(
                    "Research adapters are the next milestone. The core currently requires sourced evidence."
                )
            )
            actions.addWidget(run)
            status = QLabel("Ready")
            status.setWordWrap(True)
            layout.addWidget(brand)
            layout.addWidget(title)
            layout.addWidget(subtitle)
            layout.addSpacing(18)
            layout.addWidget(card)
            layout.addLayout(actions)
            layout.addWidget(status)
            layout.addStretch()
            self.setCentralWidget(root)
            self.setStyleSheet(
                """
                QMainWindow, QWidget { background: #f7f8fa; color: #10233f; font-size: 14px; }
                #brand { color: #a8842c; font-size: 12px; font-weight: 700; letter-spacing: 1px; }
                #title { color: #10233f; font-size: 30px; font-weight: 700; }
                #card { background: white; border: 1px solid #d9dee7; border-radius: 10px; padding: 20px; }
                QLineEdit, QComboBox, QTextEdit { background: white; border: 1px solid #bac4d2; border-radius: 6px; padding: 9px; }
                QPushButton { background: #10233f; color: white; border: 0; border-radius: 6px; padding: 11px 20px; font-weight: 700; }
                QPushButton:hover { background: #19385f; }
                """
            )

    app = QApplication(sys.argv)
    window = Window()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())

