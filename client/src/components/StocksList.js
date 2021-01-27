import React from "react";
import Item from "./Item";
import "../App.css";

export default class StocksList extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      list: [],
      alphaAsc: false,
      freqAsc: true,
      highAsc: true,
      lowAsc: true,
    };
  }
  componentDidMount() {
    this.getList();
  }
  getList = () => {
    fetch("/api")
      .then((res) => res.json())
      .then((list) => this.setState({ list }));
  };
  sortBy(key) {
    const list = this.state.list.sort(function (a, b) {
      var x = Number(a[key]) ? Number(a[key]) : a[key];
      var y = Number(b[key]) ? Number(b[key]) : b[key];
      return x < y ? -1 : x > y ? 1 : 0;
    });
    if (key === "name") {
      if (this.state.alphaAsc) {
        this.setState({ list: list.reverse(), alphaAsc: !this.state.alphaAsc });
      } else {
        this.setState({ list: list, alphaAsc: !this.state.alphaAsc });
      }
    }
    if (key === "frequency") {
      if (this.state.freqAsc) {
        this.setState({ list: list.reverse(), freqAsc: !this.state.freqAsc });
      } else {
        this.setState({ list: list, freqAsc: !this.state.freqAsc });
      }
    }
    if (key === "high") {
      if (this.state.highAsc) {
        this.setState({ list: list.reverse(), highAsc: !this.state.highAsc });
      } else {
        this.setState({ list: list, highAsc: !this.state.highAsc });
      }
    }
    if (key === "low") {
      if (this.state.lowAsc) {
        this.setState({ list: list.reverse(), lowAsc: !this.state.lowAsc });
      } else {
        this.setState({ list: list, lowAsc: !this.state.lowAsc });
      }
    }
    if (key === "chg") {
      if (this.state.chgAsc) {
        this.setState({ list: list.reverse(), chgAsc: !this.state.chgAsc });
      } else {
        this.setState({ list: list, chgAsc: !this.state.chgAsc });
      }
    }
  }
  render() {
    return (
      <div class="stocks-list">
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">
                <button
                  type="button"
                  class="toggle"
                  onClick={() => this.sortBy("name")}
                >
                  Name
                </button>
              </th>
              <th scope="col">
                <button
                  type="button"
                  class="toggle"
                  onClick={() => this.sortBy("frequency")}
                >
                  # of highs in last 30 days
                </button>
              </th>
              <th scope="col">
                <button
                  type="button"
                  class="toggle"
                  onClick={() => this.sortBy("high")}
                >
                  52 Week High
                </button>
              </th>
              <th scope="col">
                <button
                  type="button"
                  class="toggle"
                  onClick={() => this.sortBy("low")}
                >
                  52 Week Low
                </button>
              </th>
            </tr>
          </thead>
          <tbody>
            {this.state.list.map((item) => (
              <Item
                key={item.name}
                name={item.name}
                ticker={item.ticker}
                link={item.link}
                frequency={item.frequency}
                high={item.high}
                low={item.low}
              />
            ))}
          </tbody>
        </table>
      </div>
    );
  }
}
