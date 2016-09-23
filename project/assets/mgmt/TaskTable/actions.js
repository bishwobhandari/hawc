import fetch from 'isomorphic-fetch';
import h from 'mgmt/utils/helpers';

import { setError, resetError } from 'shared/actions/Errors';
import * as types from './constants';

function makeTaskRequest(){
    return {
        type: types.REQUEST_TASKS,
    };
}

function receiveTasks(tasks){
    return {
        type: types.RECEIVE_TASKS,
        tasks,
    };
}

function patchTask(task){
    return {
        type: types.PATCH_TASK,
        task,
    };
}

export function fetchTasks(){
    return (dispatch, getState) => {
        dispatch(resetError());
        let state = getState();
        if (state.tasks.isFetching) return;
        dispatch(makeTaskRequest());
        let { host, tasks } = state.config;
        const url = h.getUrlWithAssessment(h.getListUrl(host, tasks.url), state.config.assessment_id);
        return fetch(url, h.fetchGet)
            .then((response) => response.json())
            .then((json) => dispatch(receiveTasks(json)))
            .catch((error) => dispatch(setError(error)));
    };
}

function submitTaskEdit(task) {
    return (dispatch, getState) => {
        let state = getState();
        let { host, tasks } = state.config;
        const url = h.getObjectUrl(host, tasks.url, task.id),
            opts = h.fetchPost(state.config.csrf, task, 'PATCH');
        return fetch(url, opts)
            .then((response) => {
                if (response.ok){
                    response.json()
                        .then((json) => dispatch(patchTask(json)));
                } else {
                    response.json()
                        .then((json) => dispatch(setError(json)));
                }
            });
    };
}

export function submitTasks(tasks){
    return (dispatch, getState) => {
        dispatch(resetError());
        let state = getState();
        if (state.tasks.isSubmitting) return;
        Promise.all(
            tasks.map((task) => {return dispatch(submitTaskEdit(task));})
        );
    };
}

function makeStudyRequest(){
    return {
        type: types.REQUEST_STUDIES,
    };
}

function receiveStudies(studies){
    return {
        type: types.RECEIVE_STUDIES,
        studies,
    };
}

export function fetchStudies(){
    return (dispatch, getState) => {
        let state = getState();
        if (state.studies.isFetching) return;
        dispatch(makeStudyRequest());
        let { host, studies } = state.config;
        const url = h.getListUrl(host, studies.url);
        return fetch(url, h.fetchGet)
            .then((response) => response.json())
            .then((json) => dispatch(receiveStudies(json)))
            .catch((error) => dispatch(setError(error)));
    };
}
