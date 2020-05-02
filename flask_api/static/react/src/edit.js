'use strict';

class CardsContainer extends React.Component {
  state = {
    cards_data: [],
    deck_id: 0
  }

  componentDidMount() {
    this.state.deck_id = window.location.pathname.split('/').pop();
    fetch('http://127.0.0.1:5000/api/decks/'+this.state.deck_id+"/cards", 
      { method:'GET',
        headers:  new Headers({'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1ODgwOTY3MjQsIm5iZiI6MTU4ODA5NjcyNCwianRpIjoiMjY4ZjQ2MDAtNzFhZC00ZTY1LThhNjAtZTZjYzM1MmIwYzdhIiwiZXhwIjoxNTg4NzAxNTI0LCJpZGVudGl0eSI6IjVlYTQyMzMyOWM1YWZjNjA4MjBlYzA4MSIsImZyZXNoIjpmYWxzZSwidHlwZSI6ImFjY2VzcyJ9.73vHmWLDkeBVtflBVMKc-FKOY594V8z0nQ8qqsM8OyA'}),
      })
    .then(res => res.json())
    .then((data) => {
      this.setState({ cards_data: data })
    })
    .catch(console.log)
  };

  render() {
    const cards = [];
    this.state.cards_data.forEach((card) => {
      cards.push(
        <CardBox card={card} />
      );
    });
    return (
      <div className="row">
        {cards}
      </div>
    );
  }
}


class ListBox extends React.Component {
  constructor(props) {
    super(props);
  }
  render() {
    return (
      <div className="col-xl-3 col-md-6 mb-4">
        <div className={"card border-bottom-"+this.props.accent +" shadow h-100 py-2"}>
          {this.props.children}
        </div>
      </div>
    );
  }
}


class CardBox extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    // if (this.state.liked) {
    //   return 'You liked this.';
    // }

    return (
      <ListBox accent="primary">
        <div className="card-body">
            <span>{this.props.card.question}</span>
            <span>{this.props.card.answer}</span>
        </div>
      </ListBox>
    );
  }
}

ReactDOM.render(
  <CardsContainer />,
  document.querySelector('#cards_container')
);

