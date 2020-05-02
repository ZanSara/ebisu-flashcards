'use strict';

class StudyCard extends React.Component {
  state = {
    card_data: [],
    deck_id: 0 
  }

  componentDidMount() {
    this.state.deck_id = window.location.pathname.split('/').pop();
    fetch('http://127.0.0.1:5000/api/study/'+this.state.deck_id, 
      { method:'GET',
        headers:  new Headers({'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1ODgwOTY3MjQsIm5iZiI6MTU4ODA5NjcyNCwianRpIjoiMjY4ZjQ2MDAtNzFhZC00ZTY1LThhNjAtZTZjYzM1MmIwYzdhIiwiZXhwIjoxNTg4NzAxNTI0LCJpZGVudGl0eSI6IjVlYTQyMzMyOWM1YWZjNjA4MjBlYzA4MSIsImZyZXNoIjpmYWxzZSwidHlwZSI6ImFjY2VzcyJ9.73vHmWLDkeBVtflBVMKc-FKOY594V8z0nQ8qqsM8OyA'}),
      })
    .then(res => res.json())
    .then((data) => {
      this.setState({ card_data: data });
      console.log("CARD DATA:  " + card_data);
    })
    .catch(console.log)
  };

  render() {
    return (
      <div className="row">
        <div className="col-xl-6 col-lg-5 mx-auto">
          <div className="card shadow mb-4">
            <div className="card-header py-3 d-flex flex-row align-items-center justify-content-between">
              <a href="#" className="btn btn-default btn-sm"><i className="fa fa-chevron-left"></i></a>
              <span className="m-0">Card # -- </span>
              <div className="dropdown no-arrow">
                <a className="dropdown-toggle" href="#" role="button" id="dropdownMenuLink" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                  <i className="fas fa-ellipsis-v fa-sm fa-fw text-gray-400"></i>
                </a>
                <div className="dropdown-menu dropdown-menu-right shadow animated--fade-in" aria-labelledby="dropdownMenuLink">
                  <a className="dropdown-item" href="#">Modify Card</a>
                  <a className="dropdown-item" href="#">Skip Card</a>
                  <div className="dropdown-divider"></div>
                  <a className="dropdown-item" href="#">Something else</a>
                </div>
              </div>
            </div>
            <div className="card-body text-center">
              <div className="row justify-content-center py-3" >
                <div className="col-12 text-center py-3">
                  {this.state.card_data.question}
                </div>
                <div className="col-6 py-3">
                  <input type="text form-control-lg" placeholder="Your answer..." style={{width:100+"%"}}/>
                </div>
              </div>
          
              <a id="answerButton" href="#answerArea" className="btn btn-primary" data-toggle="collapse" role="button" 
                  aria-expanded="true" aria-controls="collapseCardExample" onClick="getElementById('answerButton').style.display = 'none'">
                  Click to show answer
              </a>
          
              <div className="collapse hide" id="answerArea">
                  <div className="card-body">
                      <div></div>
                      <div>
                      {this.state.card_data.answer}  
                      </div>
                      <hr />

                      <form action={"api/study/"+this.state.deck_id} method="POST">
                        <button type="submit" name="test_result" value="0" className="btn btn-danger">
                          <i className="fas fa-fw fa-times d-md-none"></i>
                          <span className="d-none d-sm-inline-block">I forgot :(</span>
                        </button>
                        <button type="submit" name="test_result" value="1" className="btn btn-success">
                          <i className="fas fa-fw fa-check d-md-none"></i>
                          <span className="d-none d-sm-inline-block">I remember!</span>
                        </button>
                      </form>
          
                  </div>
              </div>          
            </div>    
          </div>
        </div>
      </div>
    );
  }
}

ReactDOM.render(
  <StudyCard />,
  document.querySelector('#card_container')
);

