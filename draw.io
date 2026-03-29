<mxfile host="app.diagrams.net">
  <diagram name="PawPal+ UML" id="uml1">
    <mxGraphModel dx="1000" dy="1000" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="827" pageHeight="1169" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        <!-- Owner -->
        <mxCell id="2" value="Owner" style="swimlane;html=1;" vertex="1" parent="1">
          <mxGeometry x="40" y="40" width="180" height="220" as="geometry" />
        </mxCell>
        <mxCell id="3" value="+owner_id: string\n+full_name: string\n+address: string\n+preferences: string\n+available_time: string\n+number_of_pets: int\n+get_pets()\n+get_schedules()" style="text;html=1;align=left;verticalAlign=top;whiteSpace=wrap;" vertex="1" parent="2">
          <mxGeometry x="0" y="30" width="180" height="190" as="geometry" />
        </mxCell>
        <!-- Pet -->
        <mxCell id="4" value="Pet" style="swimlane;html=1;" vertex="1" parent="1">
          <mxGeometry x="300" y="40" width="200" height="260" as="geometry" />
        </mxCell>
        <mxCell id="5" value="+pet_code: string\n+name: string\n+pet_type: string\n+species: string\n+age: int\n+comment: string\n+owner_id: string\n+tasks: list\n+add_pet(pet: Pet)\n+update_pet_info(...)\n+validate_pet_info()\n+add_task(task: Task)" style="text;html=1;align=left;verticalAlign=top;whiteSpace=wrap;" vertex="1" parent="4">
          <mxGeometry x="0" y="30" width="200" height="230" as="geometry" />
        </mxCell>
        <!-- Task -->
        <mxCell id="6" value="Task" style="swimlane;html=1;" vertex="1" parent="1">
          <mxGeometry x="600" y="40" width="220" height="320" as="geometry" />
        </mxCell>
        <mxCell id="7" value="+task_id: string\n+name: string\n+duration: int\n+priority: string\n+task_type: string\n+owner_id: string\n+pet_id: string\n+completed: bool\n+status: string\n+start_time: string\n+recurrence: string\n+due_date: string\n+description: string\n+add_task(...)\n+edit_task(...)\n+mark_complete(schedule=None)\n+validate_task()" style="text;html=1;align=left;verticalAlign=top;whiteSpace=wrap;" vertex="1" parent="6">
          <mxGeometry x="0" y="30" width="220" height="290" as="geometry" />
        </mxCell>
        <!-- Schedule -->
        <mxCell id="8" value="Schedule" style="swimlane;html=1;" vertex="1" parent="1">
          <mxGeometry x="900" y="40" width="260" height="400" as="geometry" />
        </mxCell>
        <mxCell id="9" value="+schedule_id: string\n+owner_id: string\n+pet_id: string\n+tasks: List<Task>\n+constraints: dict\n+add_task_to_schedule(task: Task)\n+remove_task_from_schedule(task_id: str)\n+generate_schedule()\n+sort_by_time()\n+detect_time_conflicts()\n+filter_tasks_by_completion(completed: bool)\n+filter_tasks_by_pet_name(pet_name: str, pet_store: list)\n+explain_schedule()\n+resolve_conflicts()\n+handle_dynamic_updates(updated_task: Task)\n+add_constraint(key: str, value)\n+validate_constraints()" style="text;html=1;align=left;verticalAlign=top;whiteSpace=wrap;" vertex="1" parent="8">
          <mxGeometry x="0" y="30" width="260" height="370" as="geometry" />
        </mxCell>
        <!-- Relationships -->
        <mxCell id="10" style="edgeStyle=orthogonalEdgeStyle;endArrow=block;html=1;" edge="1" parent="1" source="2" target="4">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="11" style="edgeStyle=orthogonalEdgeStyle;endArrow=block;html=1;" edge="1" parent="1" source="4" target="6">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="12" style="edgeStyle=orthogonalEdgeStyle;endArrow=block;html=1;" edge="1" parent="1" source="8" target="6">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="13" style="edgeStyle=orthogonalEdgeStyle;endArrow=block;html=1;" edge="1" parent="1" source="8" target="2">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="14" style="edgeStyle=orthogonalEdgeStyle;endArrow=block;html=1;" edge="1" parent="1" source="8" target="4">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
