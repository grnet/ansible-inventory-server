{{/*
Return the proper Docker Image Registry Secret Names
*/}}
{{- define "ansibleInventoryServer.imagePullSecrets" -}}
{{- if .Values.ansibleInventoryServerImage.pullSecrets }}
imagePullSecrets:
{{- range .Values.ansibleInventoryServerImage.pullSecrets }}
  - name: {{ . }}
{{- end -}}
{{- end -}}
{{- end -}}

{{/*
Return the proper Ansible Inventory Server image name
*/}}
{{- define "ansibleInventoryServer.ansibleInventoryServerImage" -}}
{{- $registryName := .Values.ansibleInventoryServerImage.registry -}}
{{- $repositoryName := .Values.ansibleInventoryServerImage.repository -}}
{{- $tag := .Values.ansibleInventoryServerImage.tag | toString -}}
{{- printf "%s/%s:%s" $registryName $repositoryName $tag -}}
{{- end -}}
