import random
from typing import Dict
import streamlit as st

st.markdown("# cおc「SPの無駄遣い」")

MY_MAX_SP = 100
ENEMY_MAX_SP = 500
KICK_SUCCESS_RATE = 70
SAN_RATE = 60

def throw_dice(x: int, y: int) -> int:
    a = [random.randint(1, y) for _ in range(x)]
    return a

if __name__ == "__main__":
    if "start" not in st.session_state:
        if st.button("シナリオ開始"):
            st.session_state["start"] = 0
            st.session_state["is_not_finish"] = 0
            st.experimental_rerun()
    else:
        if "my_sp" not in st.session_state:
            st.markdown("##### 何人SPを雇えるかな？")
            if st.button("ダイスを振る"):
                my_sp = throw_dice(1, MY_MAX_SP)[0]
                st.session_state["my_sp"] = my_sp
                st.experimental_rerun()
        else:
            my_sp = st.session_state["my_sp"]
            st.write(f"あなたは{my_sp}人のSPを雇えた!")
            if "my_true_sp" not in st.session_state:
                st.markdown("##### SPは何人サボるかな？")
                if st.button("ダイスを振る"):
                    my_true_sp = throw_dice(1, my_sp)[0]
                    st.session_state["my_true_sp"] = my_true_sp
                    st.experimental_rerun()
            else:
                my_true_sp = st.session_state["my_true_sp"]
                st.write(f"{my_sp - my_true_sp}人サボったぞ！残りは{my_true_sp}人だ")
                if "enemy_sp" not in st.session_state:
                    st.session_state["enemy_sp"] = throw_dice(1, ENEMY_MAX_SP)[0]
                enemy_sp = st.session_state["enemy_sp"]
                if "enemy_true_sp" not in st.session_state:
                    st.session_state["enemy_true_sp"] = throw_dice(1, enemy_sp)[0]
                enemy_true_sp = st.session_state["enemy_true_sp"]
                st.write(f"敵が現れた！相手は{enemy_true_sp}人のSPを雇っているぞ!({enemy_sp})")
                if "my_current_sp" not in st.session_state:
                    st.session_state["my_current_sp"] = my_true_sp
                    st.session_state["enemy_current_sp"] = enemy_true_sp
                my_current_sp = st.session_state["my_current_sp"]
                enemy_current_sp = st.session_state["enemy_current_sp"]

                if "is_not_finish" in st.session_state:
                    st.markdown(f"#### 味方: {my_current_sp}人 敵: {enemy_current_sp}人")
                    if "is_battle" not in st.session_state:
                        st.button("戦闘開始！")
                        st.session_state["is_battle"] = my_true_sp
                        st.experimental_rerun()
                    else:
                        if "round" not in st.session_state:
                            st.session_state["round"] = 1
                        round = st.session_state["round"]
                        st.markdown(f"### ROUND {round}")

                        if "my_san_num" not in st.session_state:
                            st.markdown("##### 立ち向かえるかチェック！")
                            if st.button("ダイスを振る"):
                                my_san_num = len([a for a in throw_dice(my_current_sp, 100) if a <= SAN_RATE])
                                st.session_state["my_san_num"] = my_san_num
                                st.experimental_rerun()
                        else:
                            my_san_num = st.session_state["my_san_num"]
                            st.write(f"{my_san_num}人のSPが敵に立ち向かおうとしてる")

                            if "enemy_san_num" not in st.session_state:
                                enemy_san_num = len([a for a in throw_dice(enemy_current_sp, 100) if a <= SAN_RATE])
                                st.session_state["enemy_san_num"] = enemy_san_num
                                st.experimental_rerun()
                            else:
                                enemy_san_num = st.session_state["enemy_san_num"]
                                st.write(f"敵は{enemy_san_num}人のSPが構えているぞ!")
                                if "my_success_kick_num" not in st.session_state:
                                    st.markdown("##### さぁSPよ、総攻撃だ!")
                                    if st.button("ダイスを振る"):
                                        my_success_kick_num = len([a for a in throw_dice(my_san_num, 100) if a <= KICK_SUCCESS_RATE])
                                        st.session_state["my_success_kick_num"] = my_success_kick_num
                                        st.experimental_rerun()
                                else:
                                    my_success_kick_num = st.session_state["my_success_kick_num"]
                                    st.write(f"{my_success_kick_num}人のキックが当たった！")
                                    if "enemy_success_kick_num" not in st.session_state:
                                        enemy_success_kick_num = len([a for a in throw_dice(enemy_san_num, 100) if a <= KICK_SUCCESS_RATE])
                                        st.session_state["enemy_success_kick_num"] = enemy_success_kick_num
                                        st.experimental_rerun()
                                    else:
                                        enemy_success_kick_num = st.session_state["enemy_success_kick_num"]
                                        st.write(f"敵も中々やるな！{enemy_success_kick_num}人のキックが当たった！")
                                        my_current_sp -= enemy_success_kick_num
                                        enemy_current_sp -= my_success_kick_num
                                        if my_current_sp < 0:
                                            my_current_sp = 0
                                        if enemy_current_sp < 0:
                                            enemy_current_sp = 0
                                        st.session_state["my_current_sp"] = my_current_sp
                                        st.session_state["enemy_current_sp"] = enemy_current_sp
                                        st.write(f"こっちの残りSPは{my_current_sp}人、敵の残りSPは{enemy_current_sp}人だ！")

                                        if my_current_sp > 0 and enemy_current_sp > 0: 
                                            st.write("まだまだ続くぞ！")
                                            st.session_state["round"] += 1
                                            del st.session_state["my_san_num"], st.session_state["enemy_san_num"], st.session_state["my_success_kick_num"], st.session_state["enemy_success_kick_num"]
                                            if st.button("次のラウンドへ"):
                                                st.experimental_rerun()
                                        else:
                                            del st.session_state["is_not_finish"]
                                            st.experimental_rerun()
                else:
                    if my_current_sp > 0 and enemy_current_sp <= 0:
                        st.write("「き、貴様らの…勝ちだ…」")
                        st.markdown(f"### おめでとう！無事生還したよ!SPは{my_current_sp}人生き残った！")
                        st.balloons()
                    elif my_current_sp <= 0 and enemy_current_sp > 0:
                        st.write("「これで終わりだ！」")
                        st.markdown(f"### 残念！あなたは{enemy_current_sp}人に囲まれて処刑されました…次の人生では勝てるといいね！")
                    else:
                        st.write("「今日はこのくらいで勘弁してやろう…」")
                        st.markdown(f"### 何とか引き分けに持ち込めたね！次は勝てるように頑張ろう！")
                        st.snow()
                    st.write(f"Result: {my_current_sp} {enemy_current_sp}")

                    if st.button("もう一回遊べるドン！"):
                        for k in st.session_state:
                            del st.session_state[k]
                        st.experimental_rerun()
