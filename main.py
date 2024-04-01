import streamlit as st
from utils.faiss_processing import MyFaiss
import json
from utils.config import load_config

config = load_config('configs/config.yml')

file_paths = config['file_paths']

bin_file = file_paths['bin_file']
json_path = file_paths['json_path']
info_path = file_paths['info_path']
fps_path = file_paths['fps_path']

def get_session_state():
    session_state = st.session_state
    if 'scores' not in session_state:
        session_state.scores = None
    if 'infos_query' not in session_state:
        session_state.infos_query = None
    if 'image_paths' not in session_state:
        session_state.image_paths = None
    return session_state

@st.cache_resource
def search_images(text_input, k_input):
    cosine_faiss = MyFaiss(bin_file, json_path)
    scores, _, infos_query, image_paths = cosine_faiss.text_search(text_input, k=k_input)
    return scores, infos_query, image_paths

def main():
    with open(info_path, 'r') as file:
        data_img = json.load(file)

    st.set_page_config(page_title="App", layout="wide", initial_sidebar_state='collapsed')
    st.title("Ứng dụng truy vấn hình ảnh")
    st.write("Nhập truy vấn và số lượng ảnh bạn muốn hiển thị sau đó nhấn Tìm kiếm.")

    col1, col2 = st.columns([3, 1])  # 3/4 và 1/4 chiều rộng của hàng
    with col1:
        text_input = st.text_input("Nhập truy vấn tìm kiếm:", "")

    with col2:
        k_input = st.number_input("Nhập số lượng hình ảnh:", min_value=1, max_value=10000, value=500)

    col3 = st.columns([4])[0]
    with col3:
        search_button = st.button("Tìm kiếm")

    session_state = get_session_state()

    if search_button or text_input:
        scores, infos_query, image_paths = search_images(text_input, k_input)
        session_state.scores = scores
        session_state.infos_query = infos_query
        session_state.image_paths = image_paths

    if session_state.image_paths:
        st.write(f"Kết quả tìm kiếm cho truy vấn '{text_input}':")

        num_cols = 5
        num_images = len(session_state.image_paths)
        num_rows = num_images // num_cols + (1 if num_images % num_cols != 0 else 0)

        for i in range(num_rows):
            cols = st.columns(num_cols)
            for j in range(num_cols):
                idx = i * num_cols + j
                if idx < num_images:
                    image_path = '.' + session_state.image_paths[idx]
                    info_img = session_state.infos_query[idx]['scene_idx']
                    
                    words = info_img.split('/')
                    url = data_img[words[0]][words[1]]['video_metadata']['watch_url']
                    start_time = data_img[words[0]][words[1]]['lst_shot'][words[3]]['shot_time'][0]
                    

                    with cols[j]:
                        st.image(image_path, caption=idx+1, use_column_width=True, output_format="png")
                        if st.button(f"Xem Video", key=f"video_button_{idx}", use_container_width=True):
                            st.session_state['url'] = url
                            st.session_state['start_time'] = start_time
                            st.switch_page("pages/video_app.py")
                            
                            # st.video(url, start_time=int(start_time))
    elif search_button:
        st.write("Không tìm thấy hình ảnh phù hợp.")

if __name__ == "__main__":
    main()
