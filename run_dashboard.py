import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))  # Agrega la raíz

import streamlit as st
from Proyect.visual.dashboard import main

if __name__ == "__main__":
    main()
