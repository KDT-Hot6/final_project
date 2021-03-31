
const mock = {
    title: 'intent000',
    records: [{
    	answer_code : -1,
        entities: [{entity : 'E', en_index :-1}], //값 없는 경우 빈배열
        answers: [{ answer: 'A', animation_set: 2 ,answer_index: -1}],
    }]
}
const intentView = {
    state: {
        original: {},
        updateData: {},
        hasError: false,
        isLoading: false
    },
    selector: {
        title: '.intent_view_title',
        table: '.intent_view_table',
        tableBody: '.intent_view_table_body',
        entities: '.input_entity_tags_wrap',
        addEntityButton: '.button_add_entity',
    },
    onClickSave: function () {
        /**
         * 데이터 저장
         */
        console.log('onClickSave', this.state.updateData)
    },
    onLoadIntentView: function () {
        this.state.isLoading = true
        this.state.hasError = false
        const setTitle = this.setTitle.bind(this)
        const setTable = this.setTable.bind(this)

        this.getIntentViewData().then(setTitle).then(setTable)
    },
    getIntentViewData: function () {
        /**
         * 데이터 조회
         * fetch
         * https://developer.mozilla.org/ko/docs/Web/API/Fetch_API/Fetch%EC%9D%98_%EC%82%AC%EC%9A%A9%EB%B2%95
         */
        const fetchApi = Promise.resolve(data)
        return fetchApi.then(data => {
            console.log('getIntentViewData', data)
            this.initData(data)
            this.state.isLoading = false
            this.state.hasError = false
            return data
        }).catch(error => {
            console.error(error)
            this.state.isLoading = false
            this.state.hasError = true
        })
    },

    setTitle: function (data) {
        console.log('setTitle')
        const title = document.querySelector(this.selector.title)
        const titleText = data && data.title || 'No Title'
        if (title) {
            title.innerHTML = titleText
        }
        return Promise.resolve(data)
    },
    setTable: function (data = this.state.updateData) {
        console.log('setTable', data)
        const tableBodyElement = document.querySelector(this.selector.tableBody)
        tableBodyElement.innerHTML = ''
        if (data && data.records) {
            data.records.forEach((row, index) => {
                const rowElement = this.drawTableRow(index, row)
                tableBodyElement.appendChild(rowElement)
            })
        }



        return Promise.resolve(data)
    },
    isExist: function (selector) {
        return document.querySelector(selector) ? true : false
    },
    drawTableRow: function (rowIndex, { entities = [], answers = [] }) {
        const rowElement = document.createElement("tr")
        const rowId = `#intent_row_${rowIndex}`

        rowElement.id = rowId
        rowElement.innerHTML = `
                    <td>
						<div class="index">${rowIndex + 1}</div>
					</td>
					<td>
						<div class="input_entity_tags_wrap">
							${this.drawEntities(rowIndex, entities)}
						</div>
						<div>
                            <button class="button_entity_tag_add btn btn-sm" onclick="intentView.onAddEntity(${rowIndex})">
                                <i class="fal fa-plus"></i>
                                엔티티추가
                            </button>
						</div>
					</td>
					<td>
						
                        ${this.drawAnswers(rowIndex, answers)}
                    
                        <div>
                            <button class="button_add_answer btn btn-sm" onclick="intentView.onAddAnswer(${rowIndex})">
                                <i class="fal fa-plus"></i>
                                답변추가
                            </button>
                        </div>  
					</td>
					<td>
						<div class="delete_entity_wrap">
                            <button class="button_delete_entity btn btn-outline-danger btn-sm" onclick="intentView.onDeleteIntentRow(${rowIndex})">
                                줄삭제
                            </button>
						</div>
                    </td>
            `
        return rowElement
    },

    initData: function (data) {
        this.state.original = data
        this.state.updateData = data
    },

    onAddIntentRow: function () {
        console.log('onAddIntentRow')
        if (!this.state.updateData.records) {
            this.state.updateData.records = []
        }
        this.state.updateData.records.push({
            entities: [''],
            answers: [{ answer: '', animation_set: 2 }],
        })
        this.setTable()
    },
    onDeleteIntentRow: function (rowIndex = 0) {
        console.log('onDeleteIntentRow')
        let copy = [].concat(this.state.updateData.records)
        this.state.updateData.records = [].concat(copy.slice(0, rowIndex), copy.slice(rowIndex + 1, copy.length))
        this.setTable()
    },


    drawEntities: (rowIndex, entities) => {
        console.log('drawEntities', rowIndex, entities)
        return entities.map((entity = '', index) => {
            return `
            <a class="input_entity_tag input-group">
                <input value="${entity}" class="input_entity" onchange="intentView.onChangeEntity(this.value, ${rowIndex}, ${index})"></input>
                <div class="input-group-append">
                    <button onclick="intentView.onDeleteEntity(${rowIndex}, ${index})" class="button_entity_delete btn btn-outline-danger btn-sm"><i class="fal fa-times"></i></button>
                </div>
            </a>
        `
        }).join('\n')
    },
    onAddEntity: function (rowIndex = 0) {
        console.log('onAddEntity')
        if (!this.state.updateData.records[rowIndex].entities) {
            this.state.updateData.records[rowIndex].entities = ['']
        }
        this.state.updateData.records[rowIndex].entities.push('')
        this.setTable()
    },
    onChangeEntity: function (value = '', rowIndex = 0, entityIndex = 0) {
        console.log('onChangeEntity')
        this.state.updateData.records[rowIndex].entities[entityIndex] = value
    },
    onDeleteEntity: function (rowIndex = 0, entityIndex = 0) {
        let copy = [].concat(this.state.updateData.records[rowIndex].entities)
        this.state.updateData.records[rowIndex].entities = [].concat(copy.slice(0, entityIndex), copy.slice(entityIndex + 1, copy.length))
        this.setTable()
    },

    drawAnswers: function (rowIndex = 0, answers = []) {

        console.log('drawAnswers', rowIndex, answers)
        return answers.map(({ answer, animation_set }, index) => {
            return `
            <div class="input_answer_wrap input-group">
                <select value="${animation_set}" class="select_animation form-control" style="width: unset;flex: unset; padding: 4px 8px; height: 32px;" onchange="intentView.onChangeAnimation(this.value, ${rowIndex}, ${index})">
                    ${["1", "2", "3", "4", "5", "6"].map(optionValue => `<option ${optionValue == animation_set ? "selected" : ""} value="${optionValue}">${optionValue}</option>`)}
                </select>
                <textarea class="input_answer form-control" style="padding: 4px 8px;" value="${answer}" onchange="intentView.onChangeAnswer(this.value, ${rowIndex}, ${index})" oninput="intentView.autoGrow(this)">${answer}</textarea>
                <div class="input-group-append">
                    <button class="button_delete_answer btn btn-outline-danger btn-sm" onclick="intentView.onDeleteAnwser(${rowIndex}, ${index})"><i class="fal fa-times"></i></button>
                </div>
            </div>
           
            
        `
        }).join('\n')

    },

    onChangeAnswer: function (value = '', rowIndex = 0, answerIndex = 0) {
        console.log('onChangeAnswer')
        this.state.updateData.records[rowIndex].answers[answerIndex].answer = value
    },
    onChangeAnimation: function (value = '', rowIndex = 0, answerIndex = 0) {
        console.log('onChangeAnimation')
        this.state.updateData.records[rowIndex].answers[answerIndex].animation_set = value
    },
    onAddAnswer: function (rowIndex = 0) {
        console.log('onAddAnswer')
        if (!this.state.updateData.records[rowIndex].answers) {
            this.state.updateData.records[rowIndex].answers = []
        }
        this.state.updateData.records[rowIndex].answers.push({
            answer: '',
            animation_set: 2
        })
        this.setTable()
    },
    onDeleteAnwser: function (rowIndex = 0, answerIndex = 0) {
        let copy = [].concat(this.state.updateData.records[rowIndex].answers)
        this.state.updateData.records[rowIndex].answers = [].concat(copy.slice(0, answerIndex), copy.slice(answerIndex + 1, copy.length))
        this.setTable()
    },
    autoGrow(element) {
        element.style.height = "5px";
        element.style.height = (element.scrollHeight) + "px";
    }
}
