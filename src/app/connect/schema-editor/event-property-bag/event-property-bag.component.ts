import {Component, Input, EventEmitter, OnInit, Output, OnChanges} from '@angular/core';
import {UUID} from 'angular2-uuid';
import {RestService} from '../../rest.service';
import {DragulaService} from 'ng2-dragula';
import {EventProperty} from '../model/EventProperty';
import {EventPropertyNested} from '../model/EventPropertyNested';
import {EventPropertyList} from '../model/EventPropertyList';
import {EventPropertyPrimitive} from '../model/EventPropertyPrimitive';


@Component({
    selector: 'app-event-property-bag',
    templateUrl: './event-property-bag.component.html',
    styleUrls: ['./event-property-bag.component.css']
})

export class EventPropertyBagComponent implements OnInit {

    @Input() eventProperties: EventProperty[];
    @Output() eventPropertiesChange = new EventEmitter<EventProperty[]>();


    private dragularOptions: any = {
        removeOnSpill: false
    };

    constructor(private restService: RestService,
                private dragulaService: DragulaService) {
    }

    ngOnInit() {

    }

    public addPrimitiveProperty(): void {
        const uuid: string = UUID.UUID();
        const path = '/' + uuid;

        this.eventProperties.push(new EventPropertyPrimitive(uuid, undefined));
    }


    public addNestedProperty(): void {
        const uuid: string = UUID.UUID();
        const path = '/' + uuid;

        this.eventProperties.push(new EventPropertyNested(uuid, undefined));
    }


    private isEventPropertyPrimitive(instance): boolean {
        return instance instanceof EventPropertyPrimitive;
    }

    private isEventPropertyNested(instance): boolean {
        return instance instanceof EventPropertyNested;
    }

    private isEventPropertyList(instance): boolean {
        return instance instanceof EventPropertyList;
    }


}
