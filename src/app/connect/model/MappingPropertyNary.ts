import {RdfId} from '../tsonld/RdfId';
import {RdfProperty} from '../tsonld/RdfsProperty';
import {RdfsClass} from '../tsonld/RdfsClass';
import {StaticProperty} from './StaticProperty';

@RdfsClass('sp:MappingPropertyNary')
export class MappingPropertyNary extends StaticProperty {

  @RdfId
  public id: string;

  @RdfProperty('sp:elementName')
  public elementName: string;

  @RdfProperty('http://www.w3.org/2000/01/rdf-schema#label')
  public label: string;

  @RdfProperty('http://www.w3.org/2000/01/rdf-schema#description')
  public description: string;

  @RdfProperty('sp:internalName')
  public internalName: string;

  @RdfProperty('sp:mapsFrom')
  public requirementSelector: string;

  @RdfProperty('sp:mapsFromOptions')
  public mapsFromOptions: string[];

  @RdfProperty('sp:hasPropertyScope')
  public propertyScope: string;

  @RdfProperty('sp:mapsTo')
  public selectedProperty: string;


  constructor(id: string) {
      super();
      this.id = id;
  }

}
