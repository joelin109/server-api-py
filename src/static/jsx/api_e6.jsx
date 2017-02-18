class SearchFilterC extends React.Component {
    constructor(props) {
        super(props);
        this.handleChange = this.handleChange.bind(this);
    }

    handleChange(type) {
        this.props.onChange(type, 2);
    }

    render() {
        const value = this.props.value;
        const scale = this.props.scale;
        return (
            <fieldset>
                <legend>{scale}: Now is {new Date().toLocaleTimeString()}.</legend>
                <button onClick={this.handleChange.bind(this, 'js')}>
                    JavaScript >
                </button>&nbsp;&nbsp;&nbsp;
                <button onClick={this.handleChange.bind(this, 'go')}>
                    Golang >
                </button>&nbsp;&nbsp;&nbsp;
                <button onClick={this.handleChange.bind(this, 'py')}>
                    Python >
                </button>
            </fieldset>
        );
    }
}


const apiurl = 'https://api.github.com/search/repositories?q=javascript&sort=stars'
const apiurl_go = 'https://api.github.com/search/repositories?q=created:>2014-01-01 golang&sort=stars'
const apiurl_py = 'https://api.github.com/search/repositories?q=created:%3E2015-01-01%20language:python&sort=stars'
var apiurl_error = 'http://localhost:1058/content/deutsch/list'

class RepoListC extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            loading: true,
            error: null,
            data: null,
            title: 'JavaScript'
        };

        // This line is important!
        //this.handleClick = this.handleClick.bind(this, 'js');
        this.handleClickForSearch = this.handleClickForSearch.bind(this);
    }

    componentDidMount() {
        this.handleClick(this.props.name)
        RepoTitleC.setState({first: false, title: 'dsfsdf'})
    }

    handleClick(type) {
        if (type == 'js') {
            this.state.title = 'JavaScript'
            this.apiSearch(apiurl)
        }
        else if (type == 'go') {
            this.state.title = 'Golang'
            this.apiSearch(apiurl_go)
        }
        else {
            this.state.title = 'Python'
            this.apiSearch(apiurl_py)
        }
    }

    handleClickForSearch(e, i) {
        //alert(i)
        this.handleClick(e)
    }

    apiSearch(url) {
        $.get(url).then(
            result => this.setState({loading: false, data: result}),
            error => this.setState({loading: false, error: error})
        );
    }

    render() {
        // Because `this.handleClick` is bound, we can use it as an event handler.
        if (this.state.loading) {
            return (
                <main>
                    <SearchFilterC scale="Joe" value={7} onChange={this.handleClickForSearch}/>
                    <br/> <br/>

                    <span>Loading.......</span>
                </main>
            );
        }
        else if (this.state.error !== null) {
            return <span>Error: {this.state.error.message}</span>;
        }
        else {
            var repos = this.state.data.items;
            var resultlist = repos.map(function (repo, index) {
                return (
                    <li key={index}><a href={repo.html_url}>{repo.name}</a> ({repo.stargazers_count} stars)
                        <br/> {repo.description}
                        <br/><br/></li>
                );
            });

            return (
                <main>
                    <SearchFilterC scale="Joe" value={7} onChange={this.handleClickForSearch}/>

                    <h1>{this.props.name} - Most Popular {this.state.title} Projects in Github</h1>
                    <ol>{resultlist}</ol>
                </main>


            );
        }
    }
}

RepoListC.defaultProps = {
    name: 'py'
};

RepoListC.propTypes = {
    name: React.PropTypes.string
};

ReactDOM.render(
    <RepoListC/>, document.getElementById('repolist_c')
);




class RepoTitleC extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            first: true,
            title: '',
            error: null
        };

    }

    render() {
        // Because `this.handleClick` is bound, we can use it as an event handler.
        if (this.state.first) {
            return <span><h1>Most Popular JavaScript Projects in Github</h1></span>;
        }

        else {
            return <span><h1>Most Popular Python Projects in Github</h1></span>;
        }
    }
}

ReactDOM.render(
    <RepoListC/>, document.getElementById('repolist_c')
);


function tick() {
    const element = (
        <div>
            <h1>Hello, world!</h1>
            <h2>It is {new Date().toLocaleTimeString()}.</h2>
        </div>
    );
    ReactDOM.render(
        element,
        document.getElementById('repotitle_c')
    );
}

setInterval(tick, 1000);