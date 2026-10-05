import streamlit as st
import ollama
import plotly.express as px
st.set_page_config(
    page_title="Budget Explainer",
    page_icon="💰",
    layout="wide"
)
# ==================================================
# PAGE TITLE
# ==================================================

st.title("💰 Budget Explainer")

st.write(
    "Enter your monthly income and expenses to analyze your budget."
)


# ==================================================
# INPUTS
# ==================================================

income = st.number_input(
    "Monthly Income (₹)",
    min_value=0.0,
    step=1000.0
)

rent = st.number_input(
    "Rent (₹)",
    min_value=0.0,
    step=500.0
)

food = st.number_input(
    "Food (₹)",
    min_value=0.0,
    step=500.0
)

transport = st.number_input(
    "Transport (₹)",
    min_value=0.0,
    step=500.0
)

other = st.number_input(
    "Other Expenses (₹)",
    min_value=0.0,
    step=500.0
)


# ==================================================
# ANALYZE BUTTON
# ==================================================

if st.button("🔍 Analyze My Budget"):

    # ==================================================
    # CALCULATE TOTAL EXPENSES
    # ==================================================

    total_expenses = (
        rent +
        food +
        transport +
        other
    )


    # ==================================================
    # CALCULATE REMAINING MONEY
    # ==================================================

    remaining = income - total_expenses


    # ==================================================
    # CHECK INCOME
    # ==================================================

    if income > 0:

        # ==================================================
        # EXPENSE PERCENTAGE
        # ==================================================

        expense_percentage = (
            total_expenses / income
        ) * 100


        # ==================================================
        # BUDGET SUMMARY
        # ==================================================
        st.subheader("📊 Budget Summary")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "💵 Monthly Income",
                f"₹{income:,.2f}"
            )

        with col2:
            st.metric(
                "💸 Total Expenses",
                f"₹{total_expenses:,.2f}"
            )

        with col3:
            st.metric(
                "💰 Money Remaining",
                f"₹{remaining:,.2f}"
            )
        st.write(
            "You spend",
            f"{expense_percentage:.2f}%",
            "of your income."
        )
        # ==================================================
        # EXPENSE CHART
        # ==================================================
        st.subheader("💸 Where Your Money Goes")

        expense_data = {
            "Category": [
                "Rent",
                "Food",
                "Transport",
                "Other"
            ],

            "Amount": [
                rent,
                food,
                transport,
                other
            ]
        }


        if total_expenses > 0:

            fig = px.pie(
                expense_data,
                names="Category",
                values="Amount",
                title="Expense Distribution"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:

            st.info(
                "No expenses entered yet."
            )


        # ==================================================
        # BUDGET HEALTH
        # ==================================================

        st.subheader("💚 Budget Health")

        if expense_percentage <= 50:

            st.success(
                "🟢 Good Budget - "
                "You are managing your expenses well!"
            )

        elif expense_percentage <= 70:

            st.warning(
                "🟡 Moderate Budget - "
                "Keep an eye on your spending."
            )

        else:

            st.error(
                "🔴 High Spending - "
                "Try to reduce unnecessary expenses."
            )


        # ==================================================
        # SAVINGS RECOMMENDATION
        # ==================================================

        st.subheader("💰 Savings Recommendation")

        if remaining > 0:

            savings_amount = remaining * 0.20

            st.write(
                "Recommended monthly savings:",
                f"₹{savings_amount:,.2f}"
            )


            # ==================================================
            # SAVINGS GOAL
            # ==================================================

            st.subheader("🎯 Savings Goal")

            savings_goal = st.number_input(
                "Enter your savings goal (₹)",
                min_value=0.0,
                step=1000.0,
                key="savings_goal"
            )

            if savings_goal > 0:

                months_needed = (
                    savings_goal / savings_amount
                )

                st.write(
                    "Estimated time to reach your goal:",
                    f"{months_needed:.1f} months"
                )

        else:

            st.warning(
                "Your expenses are equal to or higher "
                "than your income. Try reducing expenses "
                "before saving."
            )


        # ==================================================
        # OLLAMA AI PROMPT
        # ==================================================
        prompt = f"""
        You are a friendly personal budget assistant.

        Analyze this person's monthly budget.

        Monthly income:
        ₹{income}

        Expenses:

        Rent:
        ₹{rent}

        Food:
        ₹{food}

        Transport:
        ₹{transport}

        Other expenses:
        ₹{other}

        Total expenses:
        ₹{total_expenses}

        Money remaining:
        ₹{remaining}

        Expense percentage:
        {expense_percentage:.2f}%

        Savings recommendation:
        ₹{remaining * 0.20 if remaining > 0 else 0:.2f}

        Please explain this budget in simple language.

        Give the answer using these sections:

        1. Budget Summary

        2. Spending Analysis

        3. Biggest Expense

        4. Budget Health

        5. Three Practical Suggestions

        6. Savings Advice

        Keep the explanation short,
        clear and beginner-friendly.
        """


        # ==================================================
        # OLLAMA AI
        # ==================================================

        st.subheader("🤖 AI Budget Explanation")

        try:

            response = ollama.chat(
                model="llama3.2",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            ai_response = response["message"]["content"]

            st.write(ai_response)

        except Exception as e:

            st.error(
                "Ollama could not generate the explanation."
            )

            st.error(
                str(e)
            )


        # ==================================================
        # PERSONALIZED RECOMMENDATIONS
        # ==================================================

        st.subheader("💡 Personalized Recommendations")

        if expense_percentage > 70:

            st.error(
                "Your expenses are high compared with your income."
            )

            st.write(
                "• Try reducing unnecessary expenses."
            )

            st.write(
                "• Review your food and other expenses."
            )

            st.write(
                "• Try to increase your monthly savings."
            )

        elif expense_percentage > 50:

            st.warning(
                "Your spending is moderate."
            )

            st.write(
                "• Keep tracking your monthly expenses."
            )

            st.write(
                "• Avoid unnecessary purchases."
            )

            st.write(
                "• Try to save part of your remaining income."
            )

        else:

            st.success(
                "Your spending is under control!"
            )

            st.write(
                "• Continue maintaining your current budget."
            )

            st.write(
                "• Increase your savings if possible."
            )

            st.write(
                "• Consider setting a long-term savings goal."
            )
        # ==================================================
        # DOWNLOAD BUDGET REPORT
        # ==================================================

        st.subheader("📥 Download Budget Report")

        report = f"""
        BUDGET EXPLAINER REPORT
        =======================

        Monthly Income:
        ₹{income:,.2f}

        Total Expenses:
        ₹{total_expenses:,.2f}

        Money Remaining:
        ₹{remaining:,.2f}

        Expense Percentage:
        {expense_percentage:.2f}%


        EXPENSE DETAILS
        ===============

        Rent:
        ₹{rent:,.2f}

        Food:
        ₹{food:,.2f}

        Transport:
        ₹{transport:,.2f}

        Other Expenses:
        ₹{other:,.2f}


        SAVINGS
        =======

        Recommended Monthly Savings:
        ₹{remaining * 0.20 if remaining > 0 else 0:,.2f}


        Thank you for using Budget Explainer!
        """

        st.download_button(
            label="📥 Download Budget Report",
            data=report,
            file_name="budget_report.txt",
            mime="text/plain"
        )
    else:
        st.warning(
            "⚠️ Please enter your monthly income."
        )
