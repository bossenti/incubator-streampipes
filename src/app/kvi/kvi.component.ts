import { Component, OnInit } from '@angular/core';

import { KviService } from './shared/kvi.service';
import { DataSetDescription } from '../connect/model/DataSetDescription';
import { KviConfiguration } from './shared/kvi-configuration.model';
import { PipelineTemplateDescription } from '../connect/model/PipelineTemplateDescription';
import { StaticProperty } from '../connect/model/StaticProperty';
import { PipelineTemplateInvocation } from '../connect/model/PipelineTemplateInvocation';
import { FormControl } from '@angular/forms';
import { MatDialog } from '@angular/material';
import { KviCreatedDialog } from './kvi-created/kvi-created.dialog';
import {EventSchema} from '../connect/schema-editor/model/EventSchema';

@Component({
    templateUrl: './kvi.component.html',
    styleUrls: ['./kvi.component.css']
})
export class KviComponent implements OnInit {

    dataSets: DataSetDescription[] = [];
    selectedDataSet: DataSetDescription;
    isValidDataSet: boolean = false;

    operators: PipelineTemplateDescription[];
    selectedOperator: PipelineTemplateDescription;
    isValidOperator: boolean = false;

    configurations: StaticProperty[];
    isValidConfiguration: boolean = true;

    invocationGraph: PipelineTemplateInvocation;
    isValidName: boolean = false;
    nameControl: FormControl = new FormControl();

    selectedEventSchema: EventSchema = new EventSchema();

    constructor(private kviService: KviService, public dialog: MatDialog) {
        this.kviService.getDataSets().subscribe(res => {
            this.dataSets = res;
        });
    }

    ngOnInit() {
        this.nameControl.valueChanges
            .subscribe(res => {
                this.invocationGraph.name = res;
                this.isValidName = !!res;
            });

        this.selectedDataSet = new DataSetDescription("");
    }

    selectDataSet(dataSet: DataSetDescription) {
        this.isValidDataSet = !!dataSet;
        if (this.isValidDataSet) {
            this.selectedDataSet = dataSet;
            this.selectedEventSchema = dataSet.eventSchema;
            this.kviService.getOperators(dataSet).subscribe(res => {
                this.operators = res;
            });
        }
    }

    selectOperator(operator: PipelineTemplateDescription) {
        this.isValidOperator = !!operator;
        if (this.isValidOperator) {
            this.selectedOperator = operator;
            this.kviService.getStaticProperties(this.selectedDataSet, operator).subscribe(res => {
                this.invocationGraph = res;
                this.invocationGraph.dataSetId = this.selectedDataSet.id;
                this.invocationGraph.pipelineTemplateId = this.selectedOperator.appId;
                this.configurations = res.list;
            });
        }
    }

    selectConfiguration(configuration: any) {
        // this.isValidConfiguration = !!configuration;
        this.isValidConfiguration = true;
        if (this.isValidConfiguration) {
            this.invocationGraph.list = configuration;
        }
    }

    calculateKvi() {
        let dialogRef = this.dialog.open(KviCreatedDialog, {});
        dialogRef.afterClosed().subscribe(result => {});
        this.kviService.createPipelineTemplateInvocation(this.invocationGraph);
    }

}