import React from 'react';
import './Lists.css';

// Redux Related Imports
import { connect } from 'react-redux';
import * as actions from '../../actions/listAction';
import * as tasksActions from '../../actions/taskAction';

// Configuration
import config from '../../config/dev';

class ListsComponent extends React.Component {
  constructor(props) {
    super(props)
    this.loadLists = this.loadLists.bind(this);
    this.createList = this.createList.bind(this);
    this.loadTasks = this.loadTasks.bind(this);
    this.deleteList = this.deleteList.bind(this);
    this.openAddListForm = this.openAddListForm.bind(this);
    this.showToast = this.showToast.bind(this);
    this.clearError = this.clearError.bind(this);
    this.toastTimer = null;
    this.state = { toast: null, lastError: null };
  }

  componentDidMount() {
    this.loadLists();
  }
  showToast(message, type = 'info', duration = 3000) {
    if (this.toastTimer) {
      clearTimeout(this.toastTimer);
      this.toastTimer = null;
    }
    this.setState({ toast: { message, type } });
    this.toastTimer = setTimeout(() => this.setState({ toast: null }), duration);
  }

  clearError() {
    this.setState({ lastError: null });
  }

  openAddListForm() {
    // Clear any previous values before showing the form
    this.props.setCreateListName('');
    this.props.setCreateListDescription('');
    this.props.switchShowAddList(this.props.lists && this.props.lists.showAddList);
  }

  async loadLists() {
    try {
      const resp = await fetch(`${config.baseUrl}/list/list`, {
        method: 'POST',
        headers: {
          Accept: 'application/json',
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          access_id: this.props.login && this.props.login.accessId,
        })
      });
      if (!resp.ok) {
        const text = await resp.text();
        console.error('loadLists error:', resp.status, text);
        this.setState({ lastError: `Load lists failed: ${text || resp.status}` });
        this.props.setLists([]);
        return;
      }
      const body = await resp.json();
      console.log('loadLists response:', body);
      this.props.setLists(Array.isArray(body) ? body : []);
    } catch (err) {
      console.error('loadLists exception:', err);
      this.setState({ lastError: `Load lists exception: ${err.message || err}` });
      this.props.setLists([]);
    }
  }

  async createList() {
    try {
      this.setState({ lastError: null });
      const accessId = this.props.login && this.props.login.accessId;
      const name = this.props.lists && this.props.lists.name;
      if (!accessId) {
        this.setState({ lastError: 'You must be logged in to create a list.' });
        return;
      }
      if (!name || name.trim() === '') {
        this.setState({ lastError: 'List name is required.' });
        return;
      }
      const resp = await fetch(`${config.baseUrl}/list/create`, {
        method: 'POST',
        headers: {
          Accept: 'application/json',
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          access_id: this.props.login && this.props.login.accessId,
          name: this.props.lists && this.props.lists.name,
          description: this.props.lists && this.props.lists.description,
          is_done: false
        })
      });
      if (!resp.ok) {
        const text = await resp.text();
        console.error('createList error:', resp.status, text);
        this.showToast(`Create failed: ${text || resp.status}`, 'error');
        this.setState({ lastError: `Create failed: ${text || resp.status}` });
      } else {
        const body = await resp.json();
        console.log('createList response:', body);
        this.showToast('List created', 'success');
        this.setState({ lastError: null });
      }
      await this.loadLists()
      this.props.setCreateListName('');
      this.props.setCreateListDescription('');
      this.props.switchShowAddList(this.props.lists && this.props.lists.showAddList)
    } catch (err) {
      console.error('createList exception:', err);
      this.setState({ lastError: `Create exception: ${err.message || err}` });
    }
   }

   async deleteList(id){
    try {
      const resp = await fetch(`${config.baseUrl}/list/delete`, {
        method: 'POST',
        headers: {
          Accept: 'application/json',
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          access_id: this.props.login && this.props.login.accessId,
          id: id,
        })
      });
      if (!resp.ok) {
        const text = await resp.text();
        console.error('deleteList error:', resp.status, text);
        this.showToast(`Delete failed: ${text || resp.status}`, 'error');
        this.setState({ lastError: `Delete failed: ${text || resp.status}` });
      } else {
        const body = await resp.json();
        console.log('deleteList response:', body);
        this.showToast('List deleted', 'success');
        this.setState({ lastError: null });
      }
      await this.loadLists()
    } catch (err) {
      console.error('deleteList exception:', err);
      this.setState({ lastError: `Delete exception: ${err.message || err}` });
    }
   }

   async loadTasks(listName, id) {
    try {
      const resp = await fetch(`${config.baseUrl}/task/list`, {
        method: 'POST',
        headers: {
          Accept: 'application/json',
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          access_id: this.props.login && this.props.login.accessId,
          list_id: id,
        })
      });
      if (!resp.ok) {
        const text = await resp.text();
        console.error('loadTasks error:', resp.status, text);
        this.setState({ lastError: `Load tasks failed: ${text || resp.status}` });
        this.props.setTasks([]);
        return;
      }
      const body = await resp.json();
      console.log(body)
      this.props.setTasks(Array.isArray(body) ? body : [])
      this.props.setTaskListName(listName)
      this.props.setTaskListId(id)
    } catch (err) {
      console.error('loadTasks exception:', err);
      this.setState({ lastError: `Load tasks exception: ${err.message || err}` });
      this.props.setTasks([]);
    }
   }

  render() {
    if (this.props.lists.showAddList){
      return (
        <div className="list-wrapper">
        {this.state.toast ? (
          <div style={{position: 'fixed', right: 16, top: 16, zIndex:9999}}>
            <div style={{
              background: this.state.toast.type === 'error' ? '#ffcccc' : this.state.toast.type === 'success' ? '#d4edda' : '#cce5ff',
              color: '#000',
              padding: '10px 14px',
              borderRadius: 4,
              boxShadow: '0 2px 6px rgba(0,0,0,0.2)'
            }}>{this.state.toast.message}</div>
          </div>
        ) : null}
        {this.state.lastError ? (
          <div style={{position: 'fixed', right: 16, top: 72, zIndex:9999}}>
            <div style={{
              background: '#f8d7da',
              color: '#842029',
              padding: '12px 16px',
              borderRadius: 4,
              boxShadow: '0 2px 6px rgba(0,0,0,0.2)',
              maxWidth: 360
            }}>
              <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center'}}>
                <div style={{marginRight: 12}}>{this.state.lastError}</div>
                <button style={{marginLeft: 8}} onClick={this.clearError}>X</button>
              </div>
            </div>
          </div>
        ) : null}
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Description</th>
              <th>Done?</th>
            </tr>
          </thead>
          <tbody>
            {(this.props.lists.list || []).map((data, key) => {
              return (
                <tr key={key}>
                  <td>{data.id}</td>
                  <td>{data.name}</td>
                  <td>{data.description}</td>
                  <td>{data.is_done.toString()}</td>
                  <td> <button type="button" onClick={() => this.loadTasks(data.name, data.id)}>View Tasks</button></td>
                  <td> <button type="button" onClick={() => this.deleteList(data.id)}>Delete List</button></td>
                </tr>
              )
            })}
          </tbody>
        </table>
        <button type="button" onClick={this.openAddListForm}>Add List</button>
        <div className="login-wrapper">
                <h1>Please enter List information</h1>
                <div>
                    <label>
                        <p>List Name</p>
                        <input type="text" value={(this.props.lists && this.props.lists.name) || ''} onChange={(name) => this.props.setCreateListName(name.target.value)} />
                    </label>
                    <label>
                        <p>List Description</p>
                        <input type="text" value={(this.props.lists && this.props.lists.description) || ''} onChange={(description) => this.props.setCreateListDescription(description.target.value)} />
                    </label>
                    <div>
                        <button type="button" onClick={() => this.createList()}>Create List</button>
                    </div>
                </div>
            </div>
      </div>
      )
    }
    return (
      <div className="list-wrapper">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Description</th>
              <th>Done?</th>
            </tr>
          </thead>
          <tbody>
            {(this.props.lists.list || []).map((data, key) => {
              return (
                <tr key={key}>
                  <td>{data.id}</td>
                  <td>{data.name}</td>
                  <td>{data.description}</td>
                  <td>{data.is_done.toString()}</td>
                  <td> <button type="button" onClick={() => this.loadTasks(data.name, data.id)}>View Tasks</button></td>
                  <td> <button type="button" onClick={() => this.deleteList(data.id)}>Delete List</button></td>
                </tr>
              )
            })}
          </tbody>
        </table>
        <button type="button" onClick={this.openAddListForm}>Add List</button>
      </div>
    )
  }
}
const mapStateToProps = (state) => {
  return { ...state };
};

const mapDispatchToProps = (dispatch) => {
  return {
    setLists: (lists) => dispatch(actions.setLists(lists)),
    switchShowAddList: (currentVal) => dispatch(actions.switchShowAddListForm(currentVal)),
    setCreateListName: (name) => dispatch(actions.setCreateListName(name)),
    setCreateListDescription: (description) => dispatch(actions.setCreateListDescription(description)),
    setTasks: (tasks) => dispatch(tasksActions.setTasks(tasks)),
    setTaskListName: (listName) => dispatch(tasksActions.setTaskListName(listName)),
    setTaskListId: (listId) => dispatch(tasksActions.setTaskListId(listId))

  };
};

export default connect(mapStateToProps, mapDispatchToProps)(ListsComponent);
