import streamlit as st

def main():
    st.set_page_config(page_title="Video Player App", initial_sidebar_state='collapsed')
    st.title("Phát video")

    # Lấy các tham số truy vấn
    # Lấy tham số truy vấn
    url = st.session_state.get('url', None)
    start_time = st.session_state.get('start_time', None)


    # Chuyển đổi thời gian bắt đầu sang dạng số nguyên
    start_time = int(start_time)

    if url:
        st.video(url, start_time=start_time)
    else:
        st.write("Không tìm thấy URL video.")
    if st.button(f"Quay lại", use_container_width=True):
        st.switch_page("main.py")

if __name__ == "__main__":
    main()
