export default function Item(props) {
  return (
    <tr>
      <td>{props.name} ({props.ticker ? props.ticker : "--"})</td>
      <td>{props.frequency}</td>
      <td>{props.high ? props.high : "--"}</td>
      <td>{props.low ? props.low : "--"}</td>
    </tr>
  );
}
