import React from 'react';
import ReactDOM from 'react-dom';
import PivotTableUI from 'react-pivottable/PivotTableUI';
import 'react-pivottable/pivottable.css';


class PivotTableComponent extends React.Component {
  constructor(props) {
    super(props);
    const sortAs = (order) => {
      return (a, b) => {
        return order.indexOf(a) - order.indexOf(b);
      };
    };
    const processedData = this.processData(props.data);
    const uniqueMonths = Array.from(new Set(props.data.map(row => row.trx_date)));
  const sortedMonths = uniqueMonths.sort((a, b) => {
    const [monthA, yearA] = a.split(' ');
    const [monthB, yearB] = b.split(' ');
    if (parseInt(yearA) !== parseInt(yearB)) {
        return parseInt(yearA) - parseInt(yearB);
    }
    const monthOrder = {
        "January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6,
        "July": 7, "August": 8, "September": 9, "October": 10, "November": 11, "December": 12
    };
    return monthOrder[monthA] - monthOrder[monthB];
});
    this.state = {
      pivotState: {
        data: props.data,
        rows: ["sales_person"],
        cols: ["trx_date", "segment"],
        vals: ["net_brokerage_mgmt", "brokerage_for_month_segment"],
        aggregatorName: "Sum",
        sorters: {
          // Custom sorting for trx_date
          'trx_date': sortAs(sortedMonths),
      }
    }
    };

    this.handlePivotChange = this.handlePivotChange.bind(this);
  }

  processData(data) {
    const totalBrokerageBySalesPersonAndMonth = {};

    // Process each row
    data.forEach(row => {
      const { trx_date, segment, sales_person, family_code, value } = row;
      const key = `${sales_person}-${family_code}-${trx_date}-${segment}`;
      
      if (!totalBrokerageBySalesPersonAndMonth[key]) {
        totalBrokerageBySalesPersonAndMonth[key] = {
          sales_person,
          family_code,
          trx_date,
          segment,
          value: parseFloat(value)
        };
      } else {
        totalBrokerageBySalesPersonAndMonth[key].value += parseFloat(value);
      }
    });

    // Convert the processed data to an array
    const processedData = Object.values(totalBrokerageBySalesPersonAndMonth);

    // Calculate totals and format the data
    const formattedData = [];
    const totals = {};

    processedData.forEach(row => {
      const { sales_person, family_code, trx_date, segment, value } = row;
      formattedData.push(row);

      const totalKey = `${sales_person}-${family_code}`;
      if (!totals[totalKey]) {
        totals[totalKey] = { sales_person, family_code, EQ: 0, FO: 0, Total: 0 };
      }

      totals[totalKey][segment] += value;
      totals[totalKey].Total += value;
    });

    Object.values(totals).forEach(total => {
      formattedData.push({
        sales_person: total.sales_person,
        family_code: total.family_code,
        trx_date: 'Totals',
        segment: '',
        value: total.Total
      });
    });

    return formattedData;
  }

  handlePivotChange(newState) {
    this.setState({ pivotState: newState });
  }

  render() {
    return (
      <div className="App">
        <PivotTableUI
          data={this.state.pivotState.data}
          onChange={this.handlePivotChange}
          {...this.state.pivotState}
        />
      </div>
    );
  }
}

export default function renderPivotTableComponent(element, data) {
  ReactDOM.render(<PivotTableComponent data={data} />, element);
}