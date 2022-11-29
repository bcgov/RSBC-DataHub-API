import { twentyFourHourFormJsonInfoType } from '@/types/Forms/MV2634';
import { VuexModule, Module, Mutation, Action } from 'vuex-module-decorators';

@Module({
  namespaced: true
})
class MV2634 extends VuexModule {

    public mv2634FormsJson: twentyFourHourFormJsonInfoType[] = [];
    public mv2634Info = {} as twentyFourHourFormJsonInfoType;  
    
      
    @Mutation
    public setMV2634FormsJson(mv2634FormsJson: twentyFourHourFormJsonInfoType[]): void {   
        this.mv2634FormsJson = mv2634FormsJson;
    }    
    @Action
    public UpdateMV2634FormsJson(newMV2634FormsJson: twentyFourHourFormJsonInfoType[]): void {
        this.context.commit('setMV2634FormsJson', newMV2634FormsJson);
    }
  
    @Mutation
    public setMV2634Info(mv2634Info: twentyFourHourFormJsonInfoType): void {   
        this.mv2634Info = mv2634Info;        
    }    
    @Action
    public UpdateMV2634Info(newMV2634Info: twentyFourHourFormJsonInfoType): void {
        this.context.commit('setMV2634Info', newMV2634Info);        
    } 
    
}

export default MV2634