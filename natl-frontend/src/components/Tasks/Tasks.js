import React from 'react';
import './Tasks.css';

// Redux Related Imports
import { connect } from 'react-redux';
import * as listActions from '../../actions/listAction';
import * as actions from '../../actions/taskAction';

// Configuration
import config from '../../config/dev';

class TasksComponent extends React.Component {
  constructor(props) {
    super(props)
    this.createTask= this.createTask.bind(this);
    this.loadTasks = this.loadTasks.bind(this);
    this.deleteTask = this.deleteTask.bind(this);
    this.switchTaskIsDone = this.switchTaskIsDone.bind(this);
    this.openAddTaskForm = this.openAddTaskForm.bind(this);
    this.showToast = this.showToast.bind(this);
    this.toastTimer = null;
    this.state = { toast: null, lastError: null };
    this.clearError = this.clearError.bind(this);
  }

  openAddTaskForm() {
    // Clear any previous values before showing the form
    this.props.setCreateTaskName('');
    this.props.setCreateTaskDescription('');
    this.props.switchShowAddTaskForm(this.props.tasks && this.props.tasks.showAddTaskForm);
  }

  showToast(message, type = 'info', duration = 3000) {
    // type: 'info' | 'success' | 'error'
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

  async createTask() {
    try {
      // clear any previous error
      this.setState({ lastError: null });
      // basic client-side validation
      const accessId = this.props.login && this.props.login.accessId;
      const listId = this.props.tasks && this.props.tasks.taskListId;
      const name = this.props.tasks && this.props.tasks.name;
      if (!accessId) {
        this.setState({ lastError: 'You must be logged in to create a task.' });
        return;
      }
      if (!listId) {
        this.setState({ lastError: 'Please select a list before adding a task.' });
        return;
      }
      if (!name || name.trim() === '') {
        this.setState({ lastError: 'Task name is required.' });
        return;
      }
      const resp = await fetch(`${config.baseUrl}/task/create`, {
        method: 'POST',
        headers: {
          Accept: 'application/json',
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          access_id: this.props.login && this.props.login.accessId,
          name: this.props.tasks && this.props.tasks.name,
          description: this.props.tasks && this.props.tasks.description,
          list_id: this.props.tasks && this.props.tasks.taskListId,
          is_done: false
        })
      });
      if (!resp.ok) {
        const text = await resp.text();
        console.error('createTask error:', resp.status, text);
        this.showToast(`Create failed: ${text || resp.status}`, 'error');
        this.setState({ lastError: `Create failed: ${text || resp.status}` });
      } else {
        const body = await resp.json();
        console.log('createTask response:', body);
        this.showToast('Task created', 'success');
        this.setState({ lastError: null });
      }
      await this.loadTasks(this.props.tasks && this.props.tasks.taskListId)
      // Clear inputs after successful create and close the form
      this.props.setCreateTaskName('');
      this.props.setCreateTaskDescription('');
      this.props.switchShowAddTaskForm(this.props.tasks && this.props.tasks.showAddTaskForm)
    } catch (err) {
      console.error('createTask exception:', err);
      this.setState({ lastError: `Create exception: ${err.message || err}` });
    }
   }

   async deleteTask(id){
    try {
      const resp = await fetch(`${config.baseUrl}/task/delete`, {
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
        console.error('deleteTask error:', resp.status, text);
        this.showToast(`Delete failed: ${text || resp.status}`, 'error');
        this.setState({ lastError: `Delete failed: ${text || resp.status}` });
      } else {
        const body = await resp.json();
        console.log('deleteTask response:', body);
        this.showToast('Task deleted', 'success');
        this.setState({ lastError: null });
      }
      await this.loadTasks(this.props.tasks && this.props.tasks.taskListId)
    } catch (err) {
      console.error('deleteTask exception:', err);
    }
   }

   async loadTasks(id) {
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
      console.log('loadTasks response:', body);
      this.props.setTasks(Array.isArray(body) ? body : []);
    } catch (err) {
      console.error('loadTasks exception:', err);
      this.setState({ lastError: `Load tasks exception: ${err.message || err}` });
      this.props.setTasks([]);
    }
   }

   async switchTaskIsDone(id, is_done) {
    try {
      const resp = await fetch(`${config.baseUrl}/task/isdone`, {
        method: 'POST',
        headers: {
          Accept: 'application/json',
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          access_id: this.props.login && this.props.login.accessId,
          id: id,
          is_done: is_done
        })
      });
      if (!resp.ok) {
        const text = await resp.text();
        console.error('switchTaskIsDone error:', resp.status, text);
        this.showToast(`Update failed: ${text || resp.status}`, 'error');
        this.setState({ lastError: `Update failed: ${text || resp.status}` });
      } else {
        const body = await resp.json();
        console.log('switchTaskIsDone response:', body);
        this.showToast('Task updated', 'success');
        this.setState({ lastError: null });
      }
      this.loadTasks(this.props.tasks && this.props.tasks.taskListId)
    } catch (err) {
      console.error('switchTaskIsDone exception:', err);
    }
   }

  render() {
    if (this.props.tasks.showAddTaskForm){
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
            {(this.props.tasks.tasks || []).map((data, key) => {
              return (
                <tr key={key}>
                  <td>{data.id}</td>
                  <td>{data.name}</td>
                  <td>{data.description}</td>
                  <td>{data.is_done.toString()}</td>
                  <td> <button type="button" onClick={() => this.switchTaskIsDone(data.id, !data.is_done)}>Switch Is Done</button></td>
                  <td> <button type="button" onClick={() => this.deleteTask(data.id)}>Delete Task</button></td>
                </tr>
              )
            })}
          </tbody>
        </table>
  <button type="button" onClick={this.openAddTaskForm}>Add Task</button>
        <div className="login-wrapper">
                <h1>Please enter Task information</h1>
                <div>
          <label>
            <p>Task Name</p>
            <input type="text" value={(this.props.tasks && this.props.tasks.name) || ''} onChange={(name) => this.props.setCreateTaskName(name.target.value)} />
          </label>
          <label>
            <p>Task Description</p>
            <input type="text" value={(this.props.tasks && this.props.tasks.description) || ''} onChange={(description) => this.props.setCreateTaskDescription(description.target.value)} />
          </label>
          <div>
            <button type="button" onClick={() => this.createTask()}>Create Task</button>
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
            {(this.props.tasks.tasks || []).map((data, key) => {
              return (
                <tr key={key}>
                  <td>{data.id}</td>
                  <td>{data.name}</td>
                  <td>{data.description}</td>
                  <td>{data.is_done.toString()}</td>
                  <td> <button type="button" onClick={() => this.switchTaskIsDone(data.id, !data.is_done)}>Switch Is Done</button></td>
                  <td> <button type="button" onClick={() => this.deleteTask(data.id)}>Delete Task</button></td>
                </tr>
              )
            })}
          </tbody>
        </table>
  <button type="button" onClick={this.openAddTaskForm}>Add Task</button>
      </div>
    )
  }
}
const mapStateToProps = (state) => {
  return { ...state };
};

const mapDispatchToProps = (dispatch) => {
  return {
    switchShowAddTaskForm: (currentVal) => dispatch(actions.switchShowAddTaskForm(currentVal)),
    setCreateTaskName: (name) => dispatch(actions.setCreateTaskName(name)),
    setCreateTaskDescription: (description) => dispatch(actions.setCreateTaskDescription(description)),
    setTasks: (tasks) => dispatch(actions.setTasks(tasks)),
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(TasksComponent);
