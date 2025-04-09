import streamlit as st

def calculate_rebalancing_needs(cash, shares, current_price):
    # 현재 상태 계산
    stock_value = shares * current_price
    current_ratio = stock_value / cash
    
    # 현재 상태 출력
    st.subheader("현재 포트폴리오 상태")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("예수금", f"${cash:,.2f}")
        st.metric("주식 수량", f"{shares:,}주")
    with col2:
        st.metric("주식 가치", f"${stock_value:,.2f}")
        st.metric("주식가치/예수금 비율", f"{current_ratio:.1f}배")

    # 리밸런싱 필요 여부 확인
    if current_ratio > 9.0:
        st.subheader("📉 리밸런싱 필요: 매도")
        
        # 매도 수량 계산
        shares_to_sell = 0
        while True:
            test_shares = shares - shares_to_sell
            test_cash = cash + (shares_to_sell * current_price)
            test_stock_value = test_shares * current_price
            test_ratio = test_stock_value / test_cash
            
            if test_ratio <= 9.0:
                break
                
            shares_to_sell += 1
        
        # 매도 후 상태
        new_shares = shares - shares_to_sell
        new_cash = cash + (shares_to_sell * current_price)
        new_stock_value = new_shares * current_price
        new_ratio = new_stock_value / new_cash
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("매도 필요 수량", f"{shares_to_sell}주")
            st.metric("예상 매도 금액", f"${shares_to_sell * current_price:,.2f}")
        
        st.subheader("매도 후 예상 상태")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("예수금", f"${new_cash:,.2f}")
            st.metric("주식 수량", f"{new_shares}주")
        with col2:
            st.metric("주식 가치", f"${new_stock_value:,.2f}")
            st.metric("주식가치/예수금 비율", f"{new_ratio:.1f}배")

    elif current_ratio < 8.0:
        st.subheader("📈 리밸런싱 필요: 매수")
        
        # 매수 수량 계산
        shares_to_buy = 0
        best_ratio = current_ratio
        best_shares_to_buy = 0
        
        while True:
            test_shares = shares + shares_to_buy
            test_cash = cash - (shares_to_buy * current_price)
            
            if test_cash < current_price:
                break
                
            test_stock_value = test_shares * current_price
            test_ratio = test_stock_value / test_cash
            
            if best_shares_to_buy == 0 or (test_ratio >= 8.0 and abs(test_ratio - 8.0) < abs(best_ratio - 8.0)):
                best_ratio = test_ratio
                best_shares_to_buy = shares_to_buy
            
            if test_ratio > 8.5:
                break
                
            shares_to_buy += 1
            
        shares_to_buy = best_shares_to_buy
        
        # 매수 후 상태
        new_shares = shares + shares_to_buy
        new_cash = cash - (shares_to_buy * current_price)
        new_stock_value = new_shares * current_price
        new_ratio = new_stock_value / new_cash
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("매수 필요 수량", f"{shares_to_buy}주")
            st.metric("예상 매수 금액", f"${shares_to_buy * current_price:,.2f}")
        
        st.subheader("매수 후 예상 상태")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("예수금", f"${new_cash:,.2f}")
            st.metric("주식 수량", f"{new_shares}주")
        with col2:
            st.metric("주식 가치", f"${new_stock_value:,.2f}")
            st.metric("주식가치/예수금 비율", f"{new_ratio:.1f}배")

    else:
        st.success("리밸런싱이 필요하지 않습니다! (현재 비율이 8~9배 사이)")

    # 다음 리밸런싱 기준점
    st.subheader("다음 리밸런싱 기준점")
    upper_price = (9 * cash) / shares
    lower_price = (8 * cash) / shares
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("상향 기준점", f"${upper_price:.2f}")
        st.caption("이 가격 도달 시 주식가치/예수금 비율 9배")
    with col2:
        st.metric("하향 기준점", f"${lower_price:.2f}")
        st.caption("이 가격 도달 시 주식가치/예수금 비율 8배")

def main():
    st.title("주식 리밸런싱 시뮬레이터")
    st.caption("주식가치와 예수금의 비율을 8~9배 사이로 유지하기 위한 매매 시점 계산")
    
    with st.form("rebalance_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            cash = st.number_input("예수금 (달러)", min_value=0.01, value=155.44, step=0.01)
        with col2:
            shares = st.number_input("보유 주식 수량", min_value=1, value=148, step=1)
        with col3:
            current_price = st.number_input("현재 주가 (달러)", min_value=0.01, value=8.61, step=0.01)
        
        submitted = st.form_submit_button("계산하기")
        if submitted:
            calculate_rebalancing_needs(cash, shares, current_price)

if __name__ == "__main__":
    main()