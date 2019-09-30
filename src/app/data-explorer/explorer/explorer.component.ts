/*
 * Copyright 2019 FZI Forschungszentrum Informatik
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 */

import {Component, OnInit} from '@angular/core';
import {DatalakeRestService} from '../../core-services/datalake/datalake-rest.service';
import {InfoResult} from '../../core-model/datalake/InfoResult';
import {Observable} from 'rxjs/Observable';
import {FormControl, FormGroup} from '@angular/forms';
import {map, startWith} from 'rxjs/operators';
import {MatDialog, MatSnackBar} from '@angular/material';
import {DataDownloadDialog} from './datadownloadDialog/dataDownload.dialog';

@Component({
    selector: 'sp-explorer',
    templateUrl: './explorer.component.html',
    styleUrls: ['./explorer.css'],
})
export class ExplorerComponent implements OnInit {

    myControl = new FormControl();
    infoResult: InfoResult[];
    filteredIndexInfos: Observable<InfoResult[]>;

    page: number = 0;
    //selectedIndex: string = '';
    selectedInfoResult: InfoResult = undefined;

    //timeunit selection
    selectedTimeUnit = '1 Day';

    //aggregation / advanced options
    //group by
    enableAdvanceOptions = false;
    groupbyUnit = 'd';
    groupbyValue = 1;

    //key selections
    dataKeys: string[] = [];

    //y and x axe
    yAxesKeys: [] = [];
    xAxesKey = 'time';

    downloadFormat: string = 'csv';
    isDownloading: boolean = false;

    data;

    isLoadingData;

    //user messages
    noDateFoundinTimeRange;
    noKeySelected;
    noIndexSelection;

    //custom time range
    dateRange: Date []; // [0] start, [1] end

    //Mat Group
    selectedMatGroup = new FormControl(0);


    constructor(private restService: DatalakeRestService, private snackBar: MatSnackBar, public dialog: MatDialog) {
        let dateTmp = new Date();
        this.setDateRange(dateTmp, new Date(dateTmp.getTime() - 60000 * 60 * 24));
    }

    ngOnInit(): void {
        this.restService.getAllInfos().subscribe(res => {
                this.infoResult = res;
                this.filteredIndexInfos = this.myControl.valueChanges
                    .pipe(
                        startWith(''),
                        map(value => this._filter(value))
                    );
                this.noIndexSelection = true;
            }
        );
    }

    selectTimeUnit(value) {
        this.selectedTimeUnit = value;

        if (this.selectedTimeUnit === '1 Day') {
            this.groupbyUnit = 'm';
            this.groupbyValue = 1;
        } else if (this.selectedTimeUnit === '1 Week') {
            this.groupbyUnit = 'm';
            this.groupbyValue = 30;
        } else if (this.selectedTimeUnit === '1 Month') {
            this.groupbyUnit = 'h';
            this.groupbyValue = 4;
        } else if (this.selectedTimeUnit === '1 Year') {
            this.groupbyUnit = 'h';
            this.groupbyValue = 12;
        }

     this.loadData();
    }

    loadData() {
        this.isLoadingData = true;
        this.noDateFoundinTimeRange = false;
        this.noIndexSelection = false;

        if (this.selectedTimeUnit !== 'Custom') {
            let endDateTmp = new Date();
            let startDateTmp;

            if (this.selectedTimeUnit === '1 Day') {
                startDateTmp = new Date(endDateTmp.getTime() - 60000 * 60 * 24 * 1);
            } else if (this.selectedTimeUnit === '1 Week') {
                startDateTmp = new Date(endDateTmp.getTime() - 60000 * 60 * 24 * 7);
            } else if (this.selectedTimeUnit === '1 Month') {
                startDateTmp = new Date(endDateTmp.getTime() - 60000 * 60 * 24 * 30);
            } else if (this.selectedTimeUnit === '1 Year') {
                startDateTmp = new Date(endDateTmp.getTime() - 60000 * 60 * 24 * 365);
            }
            this.setDateRange(startDateTmp, endDateTmp);
        }

        if (this.enableAdvanceOptions) {
            let groupbyUnit = this.groupbyUnit;
            let groupbyValue = this.groupbyValue;
            if (this.groupbyUnit === 'month') {
                groupbyUnit = 'w';
                groupbyValue = 4 * groupbyValue;
            } else if(this.groupbyUnit === 'year') {
                groupbyUnit = 'd';
                groupbyValue = 365 * groupbyValue;
            }
            this.restService.getData(this.selectedInfoResult.measureName, this.dateRange[0].getTime(), this.dateRange[1].getTime(), groupbyUnit, groupbyValue).subscribe(
                res => this.processReceivedData(res)
            );
        } else {
            this.restService.getDataAutoAggergation(this.selectedInfoResult.measureName, this.dateRange[0].getTime(), this.dateRange[1].getTime()).subscribe(
                res => this.processReceivedData(res)
            );
        }

    }

    processReceivedData(res) {
        if(res.events.length > 0) {
            this.data = res.events as [];
            this.noDateFoundinTimeRange = false;
            if (this.yAxesKeys.length === 0) {
                this.noKeySelected = true;
            }
        } else {
            this.data = undefined;
            this.noDateFoundinTimeRange = true;
            this.noKeySelected = false;
        }
        this.isLoadingData = false;
    }

    selectIndex(index: string) {
        this.dataKeys = [];
        this.selectedInfoResult = this._filter(index)[0];
        this.selectedInfoResult.eventSchema.eventProperties.forEach(property => {
            if (property['domainProperties'] === undefined) {
                this.dataKeys.push(property['runtimeName']);
            } else if (property.domainProperty !== 'http://schema.org/DateTime'&& property['domainProperties'][0] != 'http://schema.org/DateTime') {
                this.dataKeys.push(property['runtimeName']);
            }
        });
        this.selectKey(this.dataKeys.slice(0, 3));
        this.loadData();
    }

    selectKey(value) {
        if (this.data === undefined) {
            this.noDateFoundinTimeRange = true;
        } else {
            this.noDateFoundinTimeRange = false;
        }
        if (value.length === 0 && !this.noDateFoundinTimeRange) {
            this.noKeySelected = true;
        } else {
            this.noKeySelected = false;
        }
        this.yAxesKeys = value;

    }

    downloadDataAsFile() {
        const dialogRef = this.dialog.open(DataDownloadDialog, {
            width: '600px',
            data: {data: this.data, xAxesKey: this.xAxesKey, yAxesKeys: this.yAxesKeys, index: this.selectedInfoResult.measureName},
            panelClass: 'custom-dialog-container'

        });
    }


    handleNextPage() {
        let offset;
        if (this.selectedTimeUnit === 'Custom') {
            offset = this.dateRange[1].getTime() - this.dateRange[0].getTime();
        } else {
            if (this.selectedTimeUnit === '1 Day') {
                offset =  60000 * 60 * 24 * 1;
            } else if (this.selectedTimeUnit === '1 Week') {
                offset =  60000 * 60 * 24 * 7;
            } else if (this.selectedTimeUnit === '1 Month') {
                offset =  60000 * 60 * 24 * 30;
            } else if (this.selectedTimeUnit === '1 Year') {
                offset =  60000 * 60 * 24 * 365;
            }
            this.selectedTimeUnit = 'Custom';
        }
        this.setDateRange(new Date(this.dateRange[0].getTime() + offset), new Date(this.dateRange[1].getTime() + offset));
        this.loadData();
    }

    handlePreviousPage() {
        let offset;
        if (this.selectedTimeUnit === 'Custom') {
            offset = -(this.dateRange[1].getTime() - this.dateRange[0].getTime());
        } else {
            if (this.selectedTimeUnit === '1 Day') {
                offset =  -60000 * 60 * 24 * 1;
            } else if (this.selectedTimeUnit === '1 Week') {
                offset =  -60000 * 60 * 24 * 7;
            } else if (this.selectedTimeUnit === '1 Month') {
                offset =  -60000 * 60 * 24 * 30;
            } else if (this.selectedTimeUnit === '1 Year') {
                offset =  -60000 * 60 * 24 * 365;
            }
            this.selectedTimeUnit = 'Custom';
        }
        this.setDateRange(new Date(this.dateRange[0].getTime() + offset), new Date(this.dateRange[1].getTime() + offset));
        this.loadData();
    }

    handleFirstPage() {
        //TODO
    }

    handleLastPage() {
        //TODO
    }

    setDateRange(start, end) {
        this.dateRange = [];
        this.dateRange[0] = start;
        this.dateRange[1] = end;
    }

    openSnackBar(message: string) {
        this.snackBar.open(message, 'Close', {
            duration: 2000,
        });
    }

    _filter(value: string): InfoResult[] {
        const filterValue = value.toLowerCase();

        return this.infoResult.filter(option => option.measureName.toLowerCase().includes(filterValue));
    }
}