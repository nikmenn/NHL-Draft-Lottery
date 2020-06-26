from flask import Flask, render_template
import NHL_Lottery_Sim as nhl_lottery

app = Flask(__name__)


@app.route("/")
def home():
    lottery_prob = nhl_lottery.lottery_prob
    reverse_standings = nhl_lottery.reverse_standings(nhl_lottery.get_standings())
    reverse_standings = sorted(reverse_standings.items(), key=lambda x: x[1])
    draft_order = nhl_lottery.draft_order(
        nhl_lottery.lottery_prob, nhl_lottery.reverse_standings(nhl_lottery.get_standings()))
    return render_template("home.html", reverse_standings=reverse_standings, draft_order=draft_order)


if __name__ == "__main__":
    app.run()
